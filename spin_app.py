from enum import Enum
import PySpin
import signal
import sys
from PyQt5 import QtGui, QtCore, QtWidgets



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

   
        self.spin_widget = SpinWidget(self)

        self.main_widget = QtWidgets.QWidget(self)
        self.main_layout = QtWidgets.QVBoxLayout(self.main_widget)

        self.view_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.view_layout)
        self.view_layout.addWidget(self.spin_widget)

        self.button_layout = QtWidgets.QVBoxLayout()
        

        self.setCentralWidget(self.main_widget)

        
class QApplication(QtWidgets.QApplication):
    def __init__(self, *args, **kwargs):
        super(QApplication, self).__init__(*args, **kwargs)
        self.main_window = MainWindow()
        self.main_window.show()
        

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    app.exec_()
