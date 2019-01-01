import Graph_Util

import cpuinfo
import os
import psutil
import GPUtil
from psutil import virtual_memory
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time

# First Window

class Window(QWidget and QMainWindow):

    def __init__(self):
        super().__init__()
        self.window()

    def window(self):
        self.resize(480, 480)
        self.center()
        self.setWindowTitle('Corkscrew')
        self.statusBar()


        qbtn = QPushButton('Quit', self)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(350, 25)
        qbtn.clicked.connect(self.exit_app)

        runbtn = QPushButton('Run', self)
        runbtn.resize(runbtn.sizeHint())
        runbtn.move(350, 400)
        runbtn.clicked.connect(self.cpu_util_timer)
        runbtn.clicked.connect(self.ram_util_timer)
        runbtn.clicked.connect(self.gpu_util_timer)

        runbtn.clicked.connect(self.cpu_util_mean)
        runbtn.clicked.connect(self.gpu_util_mean)
        runbtn.clicked.connect(self.ram_util_mean)

        graph = QPushButton('Graphs', self)
        graph.resize(graph.sizeHint())
        graph.move(200, 200)
        graph.clicked.connect(self.output_util_graphs())

        graph2 = QPushButton('RAM Graphs', self)
        graph2.resize(graph2.sizeHint())
        graph2.move(200, 250)
        graph2.clicked.connect(self.output_ram_util_graphs())

# PC Buttons

        pcbtn = QPushButton('My PC', self)
        pcbtn.resize(pcbtn.sizeHint())
        pcbtn.move(40, 25)
        pcbtn.clicked.connect(self.create_window)

# Leaderboard Buttons

        leadBtn = QPushButton('Leaderboard', self)
        leadBtn.resize(leadBtn.sizeHint())
        leadBtn.move(200, 25)
        leadBtn.clicked.connect(self.create_leader_window)


        self.show()

# functions

    def exit_app(self):
        answer = QMessageBox.question(self, 'Exit', 'Are you sure?', QMessageBox.Yes | QMessageBox.No)
        if answer == QMessageBox.Yes:
            print('Application Quit')
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

    def gpu_util_mean(self):
        length = len(Graph_Util.gpu_y)
        product = 0
        for x in range(0, length):
            product = product + Graph_Util.gpu_y[x]
        mean = product / length
        rounded_mean = round(mean, 3)
        print('Average GPU utilisation =', rounded_mean,'%')

    def gpu_util_timer(self):
        for n in range(10):
            Graph_Util.gpu_y.append(GPUtil.getAvailable(maxLoad= 90))
            Graph_Util.time_x.append(n)
            time.sleep(1)
        print('gpu done')

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

#random

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
        cpu1btn.clicked.connect(self.cpu_type)
        cpu1btn.resize(cpu1btn.sizeHint())
        cpu1btn.move(40, 25)

        gpu1btn = QPushButton('GPU Type', self)
        gpu1btn.clicked.connect(self.gpu_type)
        gpu1btn.resize(gpu1btn.sizeHint())
        gpu1btn.move(40, 75)

        ramBtn = QPushButton('RAM quantity', self)
        ramBtn.resize(ramBtn.sizeHint())
        ramBtn.move(40, 125)
        ramBtn.clicked.connect(self.ram_find)


        self.show()

# functions

    def cpu_type(self):
        self.statusBar().showMessage(cpuinfo.get_cpu_info()['brand'])

    def gpu_type(self):
        self.statusBar().showmessage(GPUtil.showUtilization())

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def ram_find(self):
        mem = virtual_memory()
        lower = mem.total / 1000000000
        gigByte = round(lower, 1)
        print('RAM size = ', gigByte, 'GB')

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


