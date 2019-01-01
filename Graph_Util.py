import GUI

import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np

cpu_y = []
gpu_y = []
time_x = []

ram_y = []
ram_time_x = []

def util_graphs():
    plt = pg.plot()
    plt.addLegend()
    plt.showGrid(x=True,y=True)
    plt.setLabel('left', 'Utilisation', units='%')
    plt.setLabel('bottom', 'Time', units='s')
    plt.setWindowTitle('Utilisation %')

    line_1 = plt.plot(time_x, cpu_y, pen='b', symbol='x', symbolPen='b', symbolBrush=0.2, name='cpu')
    line_2 = plt.plot(time_x, gpu_y, pen='r', symbol='o', symbolPen='r', symbolBrush=0.2, name='gpu')

def ram_util_graph():
    plt = pg.plot()
    plt.addLegend()
    plt.showGrid(x=True,y=True)
    plt.setLabel('left', 'Utilisation', units='%')
    plt.setLabel('bottom', 'Time', units='s')
    plt.setWindowTitle('RAM Utilisation %')
    plt.plot(ram_time_x, ram_y, pen='b', symbol='x', symbolPen='b', symbolBrush=0.2, name='ram')

if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(pg.QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()


