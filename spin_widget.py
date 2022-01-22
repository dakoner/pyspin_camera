from PyQt5 import QtGui, QtCore, QtWidgets

class SpinWidget(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(SpinWidget, self).__init__(*args, **kwargs)

        self.layout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel()
        self.layout.addWidget(self.label)

        self.camera = PySpinCamera()
        self.camera.enter_acquisition_mode()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.camera_callback)
        self.timer.start(0) 
        
        self.sp = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.sp.valueChanged.connect(self.exposure_change)
        self.sp.setMinimum(0)
        self.sp.setMaximum(50000)
        self.sp.setValue(0)
        self.sp.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sp.setTickInterval(5000)
        self.layout.addWidget(self.sp)

    def exposure_change(self, value):
        if value == 0:
            print("enable auto")
            self.camera.reset_exposure()
        else:
            print('set exposure time to', value)
            self.camera.configure_exposure(value)
        return True

    def camera_callback(self):
        image = self.camera.acquire_image()
        pixmap = QtGui.QPixmap.fromImage(image)
        self.label.setPixmap(pixmap.scaledToHeight(512))