import time
from PyQt5 import QtGui, QtCore, QtWidgets
from pyspin_camera import PySpinCamera


import numpy as np

class Worker(QtCore.QThread):
   
    stateChanged = QtCore.pyqtSignal(np.ndarray, int, int, int)

    def __init__(self, camera):
        super().__init__()
        self.camera = camera

    @QtCore.pyqtSlot()
    def run(self):
        while True:
            d, width, height, stride = self.camera.acquire_image()
            self.stateChanged.emit(d, width, height, stride)

class SpinWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(SpinWidget, self).__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel()
        self.layout.addWidget(self.label)
        self.label.setFixedSize(1440,1080)

        self.camera = PySpinCamera()
        self.camera.enter_acquisition_mode()
        #print(self.camera.ExposureTime.GetMax())
        
        # self.label.setAlignment(QtCore.Qt.AlignRight)
        # self.label.setAlignment(QtCore.Qt.AlignVCenter)
        # self.label.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        # self.label.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        # self.label.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.sp = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.sp.valueChanged.connect(self.exposure_change)
        self.sp.setMinimum(0)
        self.sp.setMaximum(100000)
        self.sp.setValue(0)
        self.sp.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sp.setTickInterval(5000)
        self.layout.addWidget(self.sp)


        self.gp = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.gp.valueChanged.connect(self.gain_change)
        self.gp.setMinimum(0)
        self.gp.setMaximum(48)
        self.gp.setValue(0)
        self.gp.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.gp.setTickInterval(5)
        self.layout.addWidget(self.gp)

        self.worker = Worker(self.camera)
        self.worker.stateChanged.connect(self.camera_callback)
        self.worker.start()
        self.t0 = time.time()
        self.camera.enable_gain()

    def exposure_change(self, value):
        if value == 0:
            print("enable auto")
            self.camera.reset_exposure()
        else:
            print('set exposure time to', value)
            self.camera.configure_exposure(value)
        return True


    def gain_change(self, value):
        if value == 0:
            print("enable auto")
            self.camera.disable_gain()
        else:
            print('set exposure time to', value)
            self.camera.enable_gain()
            self.camera.configure_gain(value)
        return True

    def camera_callback(self, d, width, height, stride):
        t0 = time.time()
        #print(t0-self.t0)
        self.t0 = t0
        image = QtGui.QImage(d, width, height, stride, QtGui.QImage.Format_Grayscale8)
        pixmap = QtGui.QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)
