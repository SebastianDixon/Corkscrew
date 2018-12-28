import Graph_Util

import cpuinfo
import os
import psutil
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
        runbtn.clicked.connect(self.util_timer)

        graph = QPushButton('Graphs', self)
        graph.resize(graph.sizeHint())
        graph.move(200, 200)
        graph.clicked.connect(self.output_util_graphs())

        graph2 = QPushButton('RAM Graphs', self)
        graph2.resize(graph2.sizeHint())
        graph2.move(300, 200)
        graph2.clicked.connect(self.output_ram_util_graphs())

        random2 = QPushButton('CPU utilisation Mean', self)
        random2.resize(random2.sizeHint())
        random2.move(200, 250)
        random2.clicked.connect(self.cpu_util_mean)

        random3 = QPushButton('GPU utilisation Mean', self)
        random3.resize(random3.sizeHint())
        random3.move(200, 300)
        random3.clicked.connect(self.gpu_util_mean)

# PC Buttons

        pcbtn = QPushButton('My PC', self)
        pcbtn.resize(pcbtn.sizeHint())
        pcbtn.move(40, 25)
        pcbtn.clicked.connect(self.create_window)

        ramBtn = QPushButton('RAM quantity', self)
        ramBtn.resize(ramBtn.sizeHint())
        ramBtn.move(40, 75)
        ramBtn.clicked.connect(self.ram_quantity)

        ram_util_Btn = QPushButton('RAM utilisation', self)
        ram_util_Btn.resize(ram_util_Btn.sizeHint())
        ram_util_Btn.move(40, 125)
        ram_util_Btn.clicked.connect(self.ram_util_timer)

# Leaderboard Buttons

        leadBtn = QPushButton('Leaderboard', self)
        leadBtn.resize(leadBtn.sizeHint())
        leadBtn.move(200, 25)
        # here goes a function which opens a new window with leaderboard info from the database

        self.show()

# functions

    def exit_app(self):
        answer = QMessageBox.question(self, 'Exit', 'Are you sure?', QMessageBox.Yes | QMessageBox.No)
        if answer == QMessageBox.Yes:
            print('Application Quit')
            sys.exit()
        else:
            print('Application Not Quit')

    def cpu_util_mean(self):
        length = len(Graph_Util.cpu_y)
        product = 0
        for x in range(length):
            product = product + Graph_Util.cpu_y[x]
        mean = product / length
        print('Average CPU utilisation =', mean)

    def gpu_util_mean(self):
        length = len(Graph_Util.gpu_y)
        product = 0
        for x in range(0, length):
            product = product + Graph_Util.gpu_y[x]
        mean = product / length
        print('Average GPU utilisation =', mean)

    def util_timer(self):
        for n in range(10):
            Graph_Util.cpu_y.append(psutil.cpu_percent())
            Graph_Util.time_x.append(n)
            time.sleep(1)
        print(Graph_Util.cpu_y, Graph_Util.gpu_y, Graph_Util.time_x)

    def ram_quantity(self):
        mem = virtual_memory()
        gigByte = mem.total / 1000000000
        remainder = gigByte % 1
        ramQuantity = gigByte - remainder
        print('RAM Quantity =', ramQuantity, 'GB')

    def ram_util_timer(self):
        mem = virtual_memory()
        for z in range(10):
            Graph_Util.ram_y.append(mem.percent)
            Graph_Util.ram_time_x.append(z)
            time.sleep(1)
        print(Graph_Util.ram_y, Graph_Util.ram_time_x)

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
        self.show(PcWindow)

# Second Window


class PcWindow(QWidget and QWindow):

    def __init__(self):
        super().__init__()
        self.Secondwindow()

    def Secondwindow(self):
        self.resize(120, 240)
        self.center()
        self.setWindowTitle('My PC')

        cpu1btn = QPushButton('CPU Type', self)
        cpu1btn.clicked.connect(self.cpu_type)
        cpu1btn.resize(cpu1btn.sizeHint())
        cpu1btn.move(40, 150)


# functions

    def cpu_type(self):
        self.statusBar().showMessage(cpuinfo.get_cpu_info()['brand'])

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    execute = Window()
    sys.exit(app.exec_())


