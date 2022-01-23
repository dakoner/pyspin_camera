#!/usr/bin/python3
# run this program on the Mac to display image streams from multiple RPis
import numpy
import sys
import sdl2
import sdl2.ext
import threading
from sdl2 import events
import ctypes
from collections import deque
from simple_pyspin import Camera
import numpy as np
import cv2

def acquire(d):
    cam = Camera() # Acquire Camera
    cam.init() # Initialize camera

    cam.start() # Start recording
    while True:
        img = cam.get_array()
        d.append(img)
        
    cam.stop() # Stop recording
    cam.close() # You should explicitly clean up

def run():
    d = deque([], 10)
    th = threading.Thread(target=acquire, args=(d,))
    th.start()


    sdl2.ext.init()
    window = sdl2.ext.Window("Hello World!", size=(3840, 2160))
    window.show()
    windowSurf = sdl2.SDL_GetWindowSurface(window.window)
    windowArray = sdl2.ext.pixels3d(windowSurf.contents)
    window.maximize()

    event = events.SDL_Event()
    running = True
    while running:
        ret = events.SDL_PollEvent(ctypes.byref(event), 1)
        if ret == 1:
            if event.type == events.SDL_QUIT:
                running = False
                break

        try:
            image = d.pop()
        except IndexError:
            pass
        else:
            image = image.swapaxes(0,1)
            image = cv2.cvtColor(image,cv2.COLOR_GRAY2RGBA)
            image = cv2.resize(image, (2160,3840))
            windowArray[:, :, :] = image
            #image = np.repeat(image[..., np.newaxis].swapaxes(0,1), 4, axis=2)
            window.refresh()

        #timer.SDL_Delay(10)


    sdl2.ext.quit()
    return 0

if __name__ == "__main__":
    sys.exit(run())


