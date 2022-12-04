import time
import signal
from PyQt5 import QtCore
import numpy as np
import imagezmq
import simplejpeg
import sys
from pyspin_camera_qobject import PySpinCamera
import PySpin

IMAGE_TIMEOUT=0.01
port = 5000


class VideoSender:
    
    def __init__(self):
        super().__init__()

        self.system = PySpin.System.GetInstance()
        self.cam_list = self.system.GetCameras()
        self.cam = self.cam_list[0]
        self.camera = PySpinCamera(self.cam)
        self.camera.imageChanged.connect(self.camera_callback)

        self.camera.initialize()
        self.camera.acquisitionMode = 'Continuous'
        self.camera.autoExposureMode = True
        
        self.sender = imagezmq.ImageSender("tcp://*:{}".format(port), REQ_REP=False)
        self.camera.begin()

        self.t0 = time.time()
        
    def camera_callback(self, img, width, height, stride):
        t0 = time.time()
        if t0 - self.t0 < IMAGE_TIMEOUT:
            return
        self.t0 = t0
        img = np.array(img)
        img = img.reshape(height, width, 1)
        jpg_buffer = simplejpeg.encode_jpeg(img, quality=90, colorspace='GRAY')
        self.sender.send_jpg("image", jpg_buffer)

    # def get_image(self):
    #     cap = cv2.VideoCapture('/dev/video0', 0)
    #     port = 5000
    #     cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
    #     cap.set(cv2.CAP_PROP_FPS, FPS)
    #     cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    #     cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    #     sender = imagezmq.ImageSender("tcp://*:{}".format(port), REQ_REP=False)
    #     counter = 0
    #     t0 = time.time()
        
    #     while True:
    #         ret = cap.grab()
    #         if ret:
    #             t1 = time.time()
    #             if t1 - t0 >= IMAGE_TIMEOUT:
    #                 # self.m_pos = 0, 0, 0
    #                 ret, img = cap.retrieve()
    #                 if ret:
    #                     jpg_buffer = simplejpeg.encode_jpeg(img, quality=100, colorspace='BGR')
    #                     sender.send_jpg("", jpg_buffer)
    #                     t0 = t1
    #             counter += 1
        


class QApplication(QtCore.QCoreApplication):
    def __init__(self, *args, **kwargs):
        super(QApplication, self).__init__(*args, **kwargs)
        self.vs = VideoSender()

    
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    q = QApplication(sys.argv)
    q.exec_()
