import pyqtgraph as pg

cpu_y = []
gpu_y = [10,20,4,6,3,5,87,67,86,9]
ram_y = []
time_x = []

def util_graphs():
    try:
        plt = pg.plot()
        plt.addLegend()
        plt.showGrid(x=True,y=True)
        plt.setLabel('left', 'Utilisation', units='%')
        plt.setLabel('bottom', 'Time', units='s')
        plt.setWindowTitle('Utilisation %')
        plt.plot(time_x, cpu_y, pen='b', symbol='x', symbolPen='b', symbolBrush=0.2, name='cpu')
        plt.plot(time_x, gpu_y, pen='r', symbol='o', symbolPen='r', symbolBrush=0.2, name='gpu')
        plt.plot(time_x, ram_y, pen='g', symbol='x', symbolPen='g', symbolBrush=0.2, name='ram')
    except:
        print('no work')

if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(pg.QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()