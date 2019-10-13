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
        self.window()

    def window(self):
        self.resize(250, 250)
        self.setWindowTitle('Corkscrew')

# run

        runbtn = QPushButton('RUN, START, GO, BEGIN', self)
        runbtn.setGeometry(20, 20, 210, 30)

        runbtn.clicked.connect(self.open_heaven)
        runbtn.clicked.connect(self.cpu_util_timer)
        runbtn.clicked.connect(self.ram_util_timer)
        runbtn.clicked.connect(self.cpu_util_mean)
        runbtn.clicked.connect(self.ram_util_mean)
        runbtn.clicked.connect(self.gpu_util_mean)
        runbtn.clicked.connect(self.util_difference)

# analysis button

        graph = QPushButton('Graph', self)
        graph.resize(graph.sizeHint())
        graph.move(20, 150)
        graph.clicked.connect(self.output_util_graphs())

# PC Buttons

        pcbtn = QPushButton('My PC', self)
        pcbtn.resize(pcbtn.sizeHint())
        pcbtn.move(20, 90)
        pcbtn.clicked.connect(self.create_window)

# Leaderboard Buttons

        leadBtn = QPushButton('Results', self)
        leadBtn.resize(leadBtn.sizeHint())
        leadBtn.move(150, 90)
        leadBtn.clicked.connect(self.create_leader_window)

# Help Button

        helpBtn = QPushButton('Help', self)
        helpBtn.resize(leadBtn.sizeHint())
        helpBtn.move(150, 150)
        helpBtn.clicked.connect(self.create_help_window)

        self.show()

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
        print('')
        Database.openFile(self)
        print('')
        if cpu_average > gpu_average:
            bottle = 'CPU'
            print('bottleneck = cpu')
            Database.gpu_search_database()
        else:
            bottle = 'GPU'
            print('bottleneck = gpu')
            Database.cpu_search_database()

        self.result_box = QTextEdit(self)
        self.result_box.move(120, 0)
        self.result_box.setPlaceholderText('CPU')

# cpu

    def cpu_util_timer(self):
        for n in range(10):
            Graph.cpu_y.append(psutil.cpu_percent())
            Graph.time_x.append(n)
            time.sleep(1)
        print(Graph.cpu_y)
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

    def gpu_util_timer(self):
        for n in range(10):
            try:
                GPUs = GPUtil.getGPUs()
                gpu_load = GPUs[0].load
                Graph.gpu_y.append(gpu_load)
            except:
                Graph.gpu_y.append(pyadl.ADLDevice.getCurrentUsage())
                Graph.time_x.append(n)
            time.sleep(1)

        print(Graph.gpu_y)
        print('gpu done')

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

    def gpu_name(self):
        try:
            try:
                model = GPUtil.GPU.name
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
#        self.cpubtn.clicked.connect()
        self.cpu_rec = QTextEdit(self)
        self.cpu_rec.move(0, 30)
        self.cpu_rec.setPlaceholderText('recommended CPU(s)')

# gpu

        self.gpubtn = QPushButton('GPUs', self)
        self.gpubtn.sizeHint()
        self.gpubtn.move(0, 230)
#        self.gpubtn.clicked.connect()
        self.gpu_rec = QTextEdit(self)
        self.gpu_rec.move(0, 260)
        self.gpu_rec.setPlaceholderText('recommended GPU(s)')

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    execute = Window()
    sys.exit(app.exec_())
