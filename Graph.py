import pyqtgraph as pg

cpu_y = []
gpu_y = []
ram_y = []
time_x = []

def util_graphs():
    """
    a graph GUI is created to illustrate the utilisation differences between the core components of the system

    the data is from the functions in the GUI script which appended data to the four arrays.

    the library pyqtgraph is used to model the data

    different colours for each line make identification of key components easier
    """
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
        print('data type error')

if __name__ == '__main__':
    import sys
    if sys.flags.interactive != 1 or not hasattr(pg.QtCore, 'PYQT_VERSION'):
        pg.QtGui.QApplication.exec_()
