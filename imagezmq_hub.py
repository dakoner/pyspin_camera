# run this program on the Mac to display image streams from multiple RPis
import cv2
import imagezmq
import simplejpeg

image_hub = imagezmq.ImageHub()
while True:  # show streamed images until Ctrl-C
    rpi_name, jpg_buffer = image_hub.recv_jpg()
    image= simplejpeg.decode_jpeg( jpg_buffer, colorspace='GRAY')
    cv2.imshow(rpi_name, image) # 1 window for each RPi
    cv2.waitKey(1)
    image_hub.send_reply(b'OK')