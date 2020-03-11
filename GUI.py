import Graph
import Database
#import pyadl
import cpuinfo
import os
import psutil
import subprocess
import GPUtil
from psutil import virtual_memory
import sys
from PyQt5.QtWidgets import *
from PyQt5.Qt import QApplication
import time

bottle = ""


class Window(QWidget and QMainWindow):

    def __init__(self):
        super().__init__()
        self.widgets = []
        self.loginWindow()

    def delete_current_widgets(self):
        try:
            for _ in range(len(self.widgets)):
                if type(self.widgets[0]) is not str:
                    self.widgets[0].deleteLater()
                self.widgets.remove(self.widgets[0])

        except RuntimeError:
            print("no1")

    def show_widgets(self):
        try:
            for widget in self.widgets:
                widget.show()

        except RuntimeError:
            print("no2")

    def mainWindow(self):
        self.delete_current_widgets()
        self.resize(250, 250)
        self.setWindowTitle('Corkscrew')

        self.runBtn = QPushButton('RUN BENCHMARK', self)
        self.runBtn.setGeometry(20, 20, 210, 30)
        self.runBtn.clicked.connect(self.open_heaven)
        self.runBtn.clicked.connect(self.gpu_util_timer)

        self.runBtn.clicked.connect(self.cpu_util_timer)
        self.runBtn.clicked.connect(self.ram_util_timer)
        self.runBtn.clicked.connect(self.cpu_util_mean)
        self.runBtn.clicked.connect(self.ram_util_mean)
        self.runBtn.clicked.connect(self.gpu_util_mean)
        self.runBtn.clicked.connect(self.util_difference)

        self.graph = QPushButton('Graph', self)
        self.graph.resize(self.graph.sizeHint())
        self.graph.move(20, 150)
        self.graph.clicked.connect(self.output_util_graphs())

        self.pcBtn = QPushButton('My PC', self)
        self.pcBtn.resize(self.pcBtn.sizeHint())
        self.pcBtn.move(20, 90)
        self.pcBtn.clicked.connect(self.create_window)

        self.leadBtn = QPushButton('Results', self)
        self.leadBtn.resize(self.leadBtn.sizeHint())
        self.leadBtn.move(150, 90)
        self.leadBtn.clicked.connect(self.create_leader_window)

        self.helpBtn = QPushButton('Help', self)
        self.helpBtn.resize(self.helpBtn.sizeHint())
        self.helpBtn.move(150, 150)
        self.helpBtn.clicked.connect(self.create_help_window)

        self.delete_current_widgets()
        self.widgets = [self.runBtn, self.graph, self.pcBtn, self.leadBtn, self.helpBtn]
        self.show_widgets()
        self.show()

    # account info

    def loginWindow(self):
        self.delete_current_widgets()
        self.resize(250, 250)
        self.setWindowTitle('Corkscrew')

        self.username = QLineEdit(self)
        self.username.move(50, 35)
        self.username.resize(self.username.sizeHint())
        self.username.setPlaceholderText("Username")

        self.password = QLineEdit(self)
        self.password.move(50, 105)
        self.password.resize(self.password.sizeHint())
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setPlaceholderText("Password")

        self.log_in = QPushButton("Login", self)
        self.log_in.move(50, 175)
        self.log_in.resize(self.log_in.sizeHint())

        self.sign_up = QPushButton("Sign up", self)
        self.sign_up.move(150, 175)
        self.sign_up.resize(self.sign_up.sizeHint())

        self.sign_up.clicked.connect(lambda: self.reg_connect(self.username.text(), self.password.text()))
        self.log_in.clicked.connect(lambda: self.sign_connect(self.username.text(), self.password.text()))

        self.widgets = [self.username, self.password, self.sign_up]
        self.show_widgets()
        self.show()

    def reg_connect(self, username, password):
        db = Database.Database()
        return db.registration(username, password)

    def reject_reg(self):
        QMessageBox.about(self, "Notice", "Username invalid")
        self.show()

    def sign_connect(self, username, password):
        db = Database.Database()
        return db.login(username, password)

    # bottleneck calculator

    def util_difference(self):
        global bottle
        c_length = len(Graph.cpu_y)
        g_length = len(Graph.gpu_y)
        cpu_total = 0
        gpu_total = 0

        for i in range(c_length):
            cpu_total += Graph.cpu_y[i]
        for x in range(g_length):
            gpu_total += Graph.gpu_y[x]
        cpu_average = cpu_total / len(Graph.cpu_y)
        gpu_average = gpu_total / len(Graph.gpu_y)

        Database.Database.openFile(self)

        if cpu_average > gpu_average:
            bottle = 'CPU'
        else:
            bottle = 'GPU'

        self.note()

        self.result_box = QTextEdit(self)
        self.result_box.move(120, 0)
        self.result_box.setPlaceholderText('CPU')

    def note(self):
        db = Database.Database()

        if bottle == 'CPU':
            QMessageBox.about(self, "Notice", "Bottleneck = CPU")
            db.getGpuDetails()
        else:
            QMessageBox.about(self, "Notice", "Bottleneck = GPU")
            db.getCpuDetails()
        self.show()

    # cpu

    def cpu_util_timer(self):
        for n in range(100):
            Graph.cpu_y.append(psutil.cpu_percent())
            Graph.time_x.append(n)
            time.sleep(1)
        print(Graph.cpu_y)

    def cpu_util_mean(self):
        length = len(Graph.cpu_y)
        product = 0
        for x in range(length):
            product += Graph.cpu_y[x]
        mean = product / length
        rounded_mean = round(mean, 3)
        print('Average CPU utilisation =', rounded_mean, '%')

    # gpu

    def gpu_util_timer(self):
        for n in range(100):
            try:
                GPUs = GPUtil.getGPUs()
                gpu_load = GPUs[0].load *100
                Graph.gpu_y.append(gpu_load)
            except:
                Graph.gpu_y.append(pyadl.ADLDevice.getCurrentUsage)
                Graph.time_x.append(n)
            time.sleep(1)

        print(Graph.gpu_y)

    def gpu_util_mean(self):
        length = len(Graph.gpu_y)
        product = 0
        for x in range(0, length):
            product += Graph.gpu_y[x]
        mean = product / length
        rounded_mean = round(mean, 3)
        print('Average GPU utilisation =', rounded_mean, '%')

    # ram

    def ram_util_timer(self):
        mem = virtual_memory()
        for _ in range(100):
            Graph.ram_y.append(mem.percent)
            time.sleep(1)
        print(Graph.ram_y)

    def ram_util_mean(self):
        length = len(Graph.ram_y)
        product = 0
        for x in range(0, length):
            product += Graph.ram_y[x]
        mean = product / length
        rounded_mean = round(mean, 3)
        print('Average RAM utilisation =', rounded_mean, '%')

    # benchmark

    def open_heaven(self):
        try:
            os.startfile(
                'C:/ProgramData/Microsoft/Windows/Start Menu/'
                'Programs/Unigine/Heaven Benchmark 4.0/Heaven Benchmark 4.0.lnk')
        except:
            subprocess.call(
                ["/usr/bin/open", "-W", "-n", "-a", "/Applications/Heaven.app"])

    # random

    def output_util_graphs(self):
        return Graph.util_graphs

    def create_window(self):
        self.next = PcWindow()

    def create_leader_window(self):
        self.next = ResWindow()

    def create_help_window(self):
        self.next = HelpWindow()


class HelpWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.FourthWindow()

    def FourthWindow(self):
        self.resize(250, 250)
        self.move(500, 0)

        self.b = QPlainTextEdit(self)
        self.b.insertPlainText('1. Use Recommended Benchmark settings\n2. Save Run Benchmark\n'
                               '3. Press F12 to Start\n'
                               '4. Save Results file when finished\n5. Open Results file when prompted\n'
                               '6. Input CPU if prompted\n7. Receive Recommended parts\n\n'
                               'Settings for Benchmark:\nAPI - DirectX11\nQuality - Ultra Tesselation\n'
                               'Extreme Resolution - 1920x1080')
        self.b.move(0, 0)
        self.b.resize(250, 250)

        self.show()


class PcWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.Secondwindow()

    def Secondwindow(self):
        self.resize(250, 250)
        self.move(0,0)

 # cpu
        self.cpu1btn = QPushButton('CPU Type', self)
        self.cpu1btn.sizeHint()
        self.cpu1btn.move(0,0)
        self.cpu1btn.clicked.connect(self.cpu_name)
        self.cpu_box = QTextEdit(self)
        self.cpu_box.move(120,0)
        self.cpu_box.setPlaceholderText('CPU')

 # gpu
        self.gpu1btn = QPushButton('GPU', self)
        self.gpu1btn.sizeHint()
        self.gpu1btn.move(0, 75)
        self.gpu1btn.clicked.connect(self.gpu_name)
        self.gpu_box = QTextEdit(self)
        self.gpu_box.setPlaceholderText('GPU')
        self.gpu_box.move(120, 75)

 # ram

        self.rambtn = QPushButton('RAM', self)
        self.rambtn.sizeHint()
        self.rambtn.move(0, 150)
        self.rambtn.clicked.connect(self.ram_find)
        self.ram_box = QTextEdit(self)
        self.ram_box.move(120, 150)
        self.ram_box.setPlaceholderText('RAM')

        self.show()

 # functions

    def cpu_name(self):
        before = cpuinfo.get_cpu_info()['brand']
        after = before.split(' ')
        model = after[2].split('-')[1]
        self.cpu_box.insertPlainText(model)
        return model

    def gpu_name(self):
        try:
            try:
                GPUs = GPUtil.getGPUs()
                model = GPUs[0].name
                self.gpu_box.insertPlainText(model)
            except:
                model = str(pyadl.ADLManager.getInstance().getDevices()[0].adapterName)
                self.gpu_box.insertPlainText(model)
        except:
            self.gpu_box.insertPlainText('no gpu found')

    def ram_find(self):
        mem = virtual_memory()
        lower = mem.total / 1000000000
        gigByte = round(lower, 1)
        output = str(gigByte)
        units = ' GB'
        self.ram_box.insertPlainText(output)
        self.ram_box.insertPlainText(units)


class ResWindow(QMainWindow and QWidget): 

    def __init__(self):
        super().__init__()
        self.Thirdwindow()

    def Thirdwindow(self):
        self.resize(250, 450)
        self.setWindowTitle('Results')
        self.move(250,0)

 # cpu

        self.cpubtn = QPushButton('CPUs', self)
        self.cpubtn.sizeHint()
        self.cpubtn.move(0, 0)
        self.cpu_rec = QTextEdit(self)
        self.cpu_rec.move(0, 30)
        self.cpu_rec.setPlaceholderText('recommended CPU(s)')

 # gpu

        self.gpubtn = QPushButton('GPUs', self)
        self.gpubtn.sizeHint()
        self.gpubtn.move(0, 230)
        self.gpu_rec = QTextEdit(self)
        self.gpu_rec.move(0, 260)
        self.gpu_rec.setPlaceholderText('recommended GPU(s)')

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    execute = Window()
    sys.exit(app.exec_())
