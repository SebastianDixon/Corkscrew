import Graph_Util

import cpuinfo
import os
import psutil
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time

#First Window

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

        RANDOM = QPushButton('Graphs', self)
        RANDOM.resize(RANDOM.sizeHint())
        RANDOM.move(200, 200)
        RANDOM.clicked.connect(self.outpututilgraphs())

#PC Buttons

        PCbtn = QPushButton('My PC', self)
        PCbtn.resize(PCbtn.sizeHint())
        PCbtn.move(40, 25)
        PCbtn.clicked.connect(self.show_PcWindow)

#Leaderboard Buttons

        Leadbtn = QPushButton('Leaderboard', self)
        Leadbtn.resize(Leadbtn.sizeHint())
        Leadbtn.move(200, 25)
        # here goes a function which opens a new window with leaderboard info from the database

        self.show()

#FUNCTIONS

    def exit_app(self):
        answer = QMessageBox.question(self, 'Exit', 'Are you sure?', QMessageBox.Yes | QMessageBox.No)
        if answer == QMessageBox.Yes:
            print('Application Quit')
            sys.exit()
        else:
            print('Application Not Quit')


    def util_timer(self):
        for n in range(10):
            Graph_Util.cpu_y.append(psutil.cpu_percent())
            Graph_Util.time_x.append(n)
            time.sleep(1)
        print(Graph_Util.cpu_y, Graph_Util.gpu_y, Graph_Util.time_x)

    def outpututilgraphs(self):
        return Graph_Util.util_graphs


    def buttonClicked(self):
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def show_PcWindow(self):
        PcWindow()





#Second Window

class PcWindow(QWidget and QMainWindow):

    def __init__(self):
        super().__init__()
        self.Secondwindow()

    def Secondwindow(self):
        self.resize(240, 240)
        self.center()
        self.setWindowTitle('My PC')
        self.statusBar()

        cpu1btn = QPushButton('CPU Type', self)
        cpu1btn.clicked.connect(self.cpu_type)
        cpu1btn.resize(cpu1btn.sizeHint())
        cpu1btn.move(40, 150)

        self.show()

#FUNCTIONS

    def cpu_type(self):
        self.statusBar().showMessage(cpuinfo.get_cpu_info()['brand'])

    def show_wind(self):
        self.show(PcWindow)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    execute = Window()
    sys.exit(app.exec_())


