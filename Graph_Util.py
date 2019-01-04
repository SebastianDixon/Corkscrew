import GUI

import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np

cpu_y = []
gpu_y = [0,1,2,3,4,5,6,7,8,9]
ram_y = []
time_x = []


def util_graphs():
    plt = pg.plot()
    plt.addLegend()
    plt.showGrid(x=True,y=True)
    plt.setLabel('left', 'Utilisation', units='%')
    plt.setLabel('bottom', 'Time', units='s')
    plt.setWindowTitle('Utilisation %')
    plt.plot(time_x, cpu_y, pen='b', symbol='x', symbolPen='b', symbolBrush=0.2, name='cpu')
    plt.plot(time_x, gpu_y, pen='r', symbol='o', symbolPen='r', symbolBrush=0.2, name='gpu')
    plt.plot(time_x, ram_y, pen='g', symbol='x', symbolPen='g', symbolBrush=0.2, name='ram')

if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(pg.QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()


