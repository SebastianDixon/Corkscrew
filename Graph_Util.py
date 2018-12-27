import GUI

import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np


cpu_y = []
gpu_y = [0,1,2,3,4,5,6,7,8,9]
#filler data as gpu utilisation function not yet made
time_x = []

def util_graphs():
    plt = pg.plot()
    plt.addLegend()
    plt.showGrid(x=True,y=True)
    plt.setLabel('left', 'Utilisation', units='%')
    plt.setLabel('bottom', 'Time', units='s')
    plt.setWindowTitle('Utilisation %')

    line_1 = plt.plot(time_x, cpu_y, pen='b', symbol='x', symbolPen='b', symbolBrush=0.2, name='cpu')
    line_2 = plt.plot(time_x, gpu_y, pen='r', symbol='o', symbolPen='r', symbolBrush=0.2, name='gpu')


if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(pg.QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()
