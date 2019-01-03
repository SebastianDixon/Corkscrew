import Graph_Util

import cpuinfo
import os
import psutil
import GPUtil
from pyadl import *
from psutil import virtual_memory
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time

# First Window

class Window(QWidget and QMainWindow):

    def __init__(self):
        super().__init__()
        self.window()

    def window(self):
        self.resize(460, 450)
        self.center()
        self.setWindowTitle('Corkscrew')
        self.statusBar()

        qbtn = QPushButton('Quit', self)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(350, 50)
        qbtn.clicked.connect(self.exit_app)

        runbtn = QPushButton('Utilisation', self)
        runbtn.resize(runbtn.sizeHint())
        runbtn.move(350, 400)
        runbtn.clicked.connect(self.cpu_util_timer)
        runbtn.clicked.connect(self.ram_util_timer)
        runbtn.clicked.connect(self.A_gpu_util_timer)

        runbtn.clicked.connect(self.cpu_util_mean)
        runbtn.clicked.connect(self.ram_util_mean)
        runbtn.clicked.connect(self.gpu_util_mean)

        heaven = QPushButton('Benchmark', self)
        heaven.resize(heaven.sizeHint())
        heaven.move(350, 350)
        heaven.clicked.connect(self.open_heaven)

# analysis button

        dropDown = QComboBox(self)
        dropDown.addItem('Nvidia')
        dropDown.addItem('AMD')
        dropDown.setObjectName('GPU brand')
        dropDown.setGeometry(250, 350, 90, 25)

        graph = QPushButton('CPU/GPU Graph', self)
        graph.resize(graph.sizeHint())
        graph.move(200, 200)
        graph.clicked.connect(self.output_util_graphs())

        graph2 = QPushButton('RAM Graph', self)
        graph2.resize(graph2.sizeHint())
        graph2.move(200, 250)
        graph2.clicked.connect(self.output_ram_util_graphs())

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

# cpu

    def cpu_util_timer(self):
        for n in range(10):
            Graph_Util.cpu_y.append(psutil.cpu_percent())
            Graph_Util.time_x.append(n)
            time.sleep(1)
        print('cpu done')

    def cpu_util_mean(self):
        length = len(Graph_Util.cpu_y)
        product = 0
        for x in range(length):
            product = product + Graph_Util.cpu_y[x]
        mean = product / length
        rounded_mean = round(mean, 3)
        print('Average CPU utilisation =', rounded_mean,'%')

# gpu

    def N_gpu_util_timer(self):
        for n in range(10):
            GPUs = GPUtil.getGPUs()
            gpu_load = GPUs[0].load
            Graph_Util.gpu_y.append(gpu_load)
            Graph_Util.time_x.append(n)
            time.sleep(1)
        print(Graph_Util.gpu_y)
        print('gpu done')

    def A_gpu_util_timer(self):
        for n in range(10):
            Graph_Util.gpu_y.append(ADLDevice.getCurrentUsage)
            Graph_Util.time_x.append(n)
            time.sleep(1)
        print(Graph_Util.gpu_y)
        print('gpu done')

#    def gpu_choice(self):
#        if choice == ('Nvidia'):
#            self.N_gpu_util_timer()
#        else:
#            self.A_gpu_util_timer()

    def gpu_util_mean(self):
        length = len(Graph_Util.gpu_y)
        product = 0
        for x in range(0, length):
            product = product + Graph_Util.gpu_y[x]
        mean = product / length
        rounded_mean = round(mean, 3)
        print('Average GPU utilisation =', rounded_mean,'%')

# ram

    def ram_util_mean(self):
        length = len(Graph_Util.ram_y)
        product = 0
        for x in range(0, length):
            product = product + Graph_Util.ram_y[x]
        mean = product / length
        rounded_mean = round(mean, 3)
        print('Average RAM utilisation =', rounded_mean,'%')

    def ram_util_timer(self):
        mem = virtual_memory()
        for z in range(10):
            Graph_Util.ram_y.append(mem.percent)
            Graph_Util.ram_time_x.append(z)
            time.sleep(1)
        print('ram done')

# benchmark

    def open_heaven(self):
        os.startfile('C:/ProgramData/Microsoft/Windows/Start Menu/Programs/Unigine/Heaven Benchmark 4.0/Heaven Benchmark 4.0.lnk')

# random

    def output_util_graphs(self):
        return Graph_Util.util_graphs

    def output_ram_util_graphs(self):
        return Graph_Util.ram_util_graph

    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def create_window(self):
        self.next = PcWindow()

    def create_leader_window(self):
        self.next = LeadWindow()

# Second Window


class PcWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.Secondwindow()

    def Secondwindow(self):
        self.resize(350, 480)
        self.center()
        self.setWindowTitle('My PC')


        cpu1btn = QPushButton('CPU Type', self)
        cpu1btn.clicked.connect(self.cpu_name)
        cpu1btn.resize(cpu1btn.sizeHint())
        cpu1btn.move(40, 25)

        gpu1btn = QPushButton('AMD GPU Type', self)
        gpu1btn.clicked.connect(self.A_gpu_name)
        gpu1btn.resize(gpu1btn.sizeHint())
        gpu1btn.move(40, 75)

        ramBtn = QPushButton('RAM quantity', self)
        ramBtn.resize(ramBtn.sizeHint())
        ramBtn.move(40, 125)
        ramBtn.clicked.connect(self.ram_find)


        self.show()

# functions

    def cpu_name(self):
        print('CPU = ',cpuinfo.get_cpu_info()['brand'])

    def A_gpu_name(self):
        print('GPU = ', ADLManager.getInstance().getDevices()[0].adapterName)

    def ram_find(self):
        mem = virtual_memory()
        lower = mem.total / 1000000000
        gigByte = round(lower, 1)
        print('RAM = ', gigByte, 'GB')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

# Third Window


class LeadWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.Thirdwindow()

    def Thirdwindow(self):
        self.resize(350, 480)
        self.center()
        self.setWindowTitle('Leaderboard')

        self.show()

# functions

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    execute = Window()
    sys.exit(app.exec_())


