import time
from PyQt5 import QtGui, QtCore, QtWidgets
from pyspin_camera_qobject import PySpinCamera
import PySpin

import numpy as np

class SpinWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(SpinWidget, self).__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel()
        self.layout.addWidget(self.label)
        self.label.setFixedSize(1440,1080)


        self.system = PySpin.System.GetInstance()
        self.cam_list = self.system.GetCameras()
        self.cam = self.cam_list[0]
        self.camera = PySpinCamera(self.cam)

        self.camera.imageChanged.connect(self.camera_callback)
        
        self.camera.initialize()
        self.camera.acquisitionMode = 'Continuous'
        self.camera.autoExposureMode = False
        self.camera.exposure=5.0

        self.camera.begin()
    

        #self.camera.enter_acquisition_mode()
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

    def exposure_change(self, value):
        if value == 0:
            print("enable auto")
            self.camera.autoExposureMode = True
        else:
            print('set exposure time to', value)
            self.camera.autoExposureMode = False
            self.camera.exposure = value
        return True


    def gain_change(self, value):
        if value == 0:
            print("enable auto")
        else:
            print('set exposure time to', value)
            self.camera.configure_gain(value)
        return True

    def camera_callback(self, d, width, height, stride):
        t0 = time.time()
        #print(t0-self.t0)
        self.t0 = t0
        image = QtGui.QImage(d, width, height, stride, QtGui.QImage.Format_Grayscale8)
        pixmap = QtGui.QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)
