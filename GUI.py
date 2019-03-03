import Graph
import Database

# import pyadl
import cpuinfo
import os
import psutil
import subprocess
import GPUtil
from psutil import virtual_memory
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time
from bs4 import BeautifulSoup

# ------------------ First Window -------------------


class Window(QWidget and  QMainWindow):


    def __init__(self):
        super().__init__()
        self.window()

    def window(self):
        self.resize(460, 450)
        self.center()
        self.setWindowTitle('Corkscrew')
        self.statusBar()

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor("#a42600"))
        self.setPalette(palette)

        qbtn = QPushButton('Quit', self)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(350, 50)
        qbtn.clicked.connect(self.exit_app)

        runbtn = QPushButton('Run', self)
        runbtn.resize(runbtn.sizeHint())
        runbtn.move(350, 400)

#        runbtn.clicked.connect(self.gpu_dropDown)
        runbtn.clicked.connect(self.cpu_util_timer)
        runbtn.clicked.connect(self.ram_util_timer)
        runbtn.clicked.connect(self.cpu_util_mean)
        runbtn.clicked.connect(self.ram_util_mean)
#        runbtn.clicked.connect(self.gpu_util_mean)
        runbtn.clicked.connect(self.openFile2)
        runbtn.clicked.connect(self.input_database2)


        heaven = QPushButton('Benchmark', self)
        heaven.resize(heaven.sizeHint())
        heaven.move(350, 350)
        heaven.clicked.connect(self.open_heaven)

# analysis button

        graph = QPushButton('Graph', self)
        graph.resize(graph.sizeHint())
        graph.move(200, 200)
        graph.clicked.connect(self.output_util_graphs())

# PC Buttons

        Pc_Title = QLabel("PC", self)
        Pc_Title.move(75, 20)

        pcbtn = QPushButton('Pc Summary', self)
        pcbtn.resize(pcbtn.sizeHint())
        pcbtn.move(40, 50)
        pcbtn.clicked.connect(self.create_window)

# Leaderboard Buttons

        Lead_Title = QLabel("Leaderboard", self)
        Lead_Title.move(210, 20)

        leadBtn = QPushButton('Ranking', self)
        leadBtn.resize(leadBtn.sizeHint())
        leadBtn.move(200, 50)
        leadBtn.clicked.connect(self.create_leader_window)

        self.show()

# functions

    def exit_app(self):
        answer = QMessageBox.question(self, 'Exit', 'Are you sure?', QMessageBox.Yes | QMessageBox.No)
        if answer == QMessageBox.Yes:
            sys.exit()
        else:
            print('Application Not Quit')

    def openFile2(self):
        return Database.openFile(self)

    def input_database2(self):
        return Database.write_database()


# cpu

    def cpu_util_timer(self):
        for n in range(10):
            Graph.cpu_y.append(psutil.cpu_percent())
            Graph.time_x.append(n)
            time.sleep(1)
        print(Graph.cpu_y)
        print(Graph.time_x)
        print('cpu done')

    def cpu_util_mean(self):
        length = len(Graph.cpu_y)
        product = 0
        for x in range(length):
            product = product + Graph.cpu_y[x]
        mean = product / length
        rounded_mean = round(mean, 3)
        print('Average CPU utilisation =', rounded_mean,'%')

# gpu

    def gpu_dropDown(self):
        items = ('Nvidia', 'AMD')
        item, okPressed = QInputDialog.getItem(self, "Get item", "GPU:", items, 0, False)
        if okPressed and item:
            print(item)
            if item == ('Nvidia'):
                self.N_gpu_util_timer()
            else:
                self.A_gpu_util_timer()

    def N_gpu_util_timer(self):
        for n in range(10):
            GPUs = GPUtil.getGPUs()
            gpu_load = GPUs[0].load
            Graph.gpu_y.append(gpu_load)
            time.sleep(1)
        print(Graph.gpu_y)
        print('N gpu done')

    def A_gpu_util_timer(self):
        for n in range(10):
            Graph.gpu_y.append(pyadl.ADLDevice.getCurrentUsage())
            Graph.time_x.append(n)
            time.sleep(1)
        print(Graph.gpu_y)
        print('A gpu done')

    def gpu_util_mean(self):
        length = len(Graph.gpu_y)
        product = 0
        for x in range(0, length):
            product = product + Graph.gpu_y[x]
        mean = product / length
        rounded_mean = round(mean, 3)
        print('Average GPU utilisation =', rounded_mean,'%')

# ram

    def ram_util_timer(self):
        mem = virtual_memory()
        for x in range(10):
            Graph.ram_y.append(mem.percent)
            time.sleep(1)
        print(Graph.ram_y)
        print(Graph.time_x)
        print('ram done')

    def ram_util_mean(self):
        length = len(Graph.ram_y)
        product = 0
        for x in range(0, length):
            product = product + Graph.ram_y[x]
        mean = product / length
        rounded_mean = round(mean, 3)
        print('Average RAM utilisation =', rounded_mean,'%')

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

    def openFile2(self):
        return Database.openFile(self)

    def input_database2(self):
        return Database.write_database()

    def read_database2(self):
        return Database.read_database_prompt()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_window(self):
        self.next = PcWindow()

    def create_leader_window(self):
        self.next = LeadWindow()


class PcWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.Secondwindow()

    def Secondwindow(self):
        self.resize(240, 450)
        self.center()

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor("#a2a400"))
        self.setPalette(palette)

#cpu
        self.cpu1btn = QPushButton('CPU Type', self)
        self.cpu1btn.sizeHint()
        self.cpu1btn.move(0,0)
        self.cpu1btn.clicked.connect(self.cpu_name)
        self.cpu_box = QTextEdit(self)
        self.cpu_box.move(120,0)
        self.cpu_box.setPlaceholderText('CPU')

#gpu
        self.gpu1btn = QPushButton('AMD GPU', self)
        self.gpu1btn.sizeHint()
        self.gpu1btn.move(0, 120)
        self.gpu1btn.clicked.connect(self.A_gpu_name)
        self.gpu_box = QTextEdit(self)
        self.gpu_box.setPlaceholderText('GPU')
        self.gpu_box.move(120, 120)

        self.gpu2btn = QPushButton('NVIDIA GPU', self)
        self.gpu2btn.sizeHint()
        self.gpu2btn.move(0, 240)
        self.gpu2btn.clicked.connect(self.N_gpu_name)
        self.gpu2_box = QTextEdit(self)
        self.gpu2_box.setPlaceholderText('GPU')
        self.gpu2_box.move(120, 240)

#ram
        self.rambtn = QPushButton('RAM', self)
        self.rambtn.sizeHint()
        self.rambtn.move(0, 360)
        self.rambtn.clicked.connect(self.ram_find)
        self.ram_box = QTextEdit(self)
        self.ram_box.move(120, 360)
        self.ram_box.setPlaceholderText('RAM')

        self.show()

    # functions

    def cpu_name(self):
        before = cpuinfo.get_cpu_info()['brand']
        after = before.split(' ')
        model = after[2].split('-')[1]
        self.cpu_box.insertPlainText(model)

    def A_gpu_name(self):
        try:
            output = str(pyadl.ADLManager.getInstance().getDevices()[0].adapterName)
            self.gpu_box.insertPlainText(output)
        except:
            self.gpu_box.insertPlainText('amd gpu')

    def N_gpu_name(self):
        try:
            output = GPUtil.GPU.name
            self.gpu2_box.insertPlainText(output)
        except:
            self.gpu2_box.insertPlainText('nvidia gpu')



    def ram_find(self):
        mem = virtual_memory()
        lower = mem.total / 1000000000
        gigByte = round(lower, 1)
        output = str(gigByte)
        units = ' GB'
        self.ram_box.insertPlainText(output)
        self.ram_box.insertPlainText(units)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class LeadWindow(QMainWindow and QWidget):

    def __init__(self):
        super().__init__()
        self.Thirdwindow()

    def Thirdwindow(self):
        self.resize(350, 480)
        self.center()
        self.setWindowTitle('Leaderboard')

        palette = QPalette()
        palette.setColor(QPalette.Background, QColor("#f441f4"))
        self.setPalette(palette)

        file = QPushButton('Write Lead.', self)
        file.resize(file.sizeHint())
        file.move(100, 100)
        file.clicked.connect(self.openFile2)
        file.clicked.connect(self.input_database2)

        file3 = QPushButton('CPU search.', self)
        file3.resize(file3.sizeHint())
        file3.move(100, 200)
        file3.clicked.connect(self.cpu_search_database2)

        file4 = QPushButton('GPU search.', self)
        file4.resize(file4.sizeHint())
        file4.move(200, 200)
        file4.clicked.connect(self.gpu_search_database2)

        self.show()

# functions

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def openFile2(self):
        return Database.openFile(self)

    def input_database2(self):
        return Database.write_database()

    def cpu_search_database2(self):
        return Database.cpu_search_database()

    def gpu_search_database2(self):
        return Database.gpu_search_database()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    execute = Window()
    sys.exit(app.exec_())