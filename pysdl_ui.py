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
def acquire(d):
    cam = Camera() # Acquire Camera
    cam.init() # Initialize camera

    cam.start() # Start recording
    while True:
        img = cam.get_array()
        print(img.shape)
        d.append(np.repeat(img[..., np.newaxis].swapaxes(0,1), 4, axis=2))

    cam.stop() # Stop recording
    cam.close() # You should explicitly clean up

def run():
    d = deque([], 2)
    th = threading.Thread(target=acquire, args=(d,))
    th.start()


    sdl2.ext.init()
    window = sdl2.ext.Window("Hello World!", size=(1440, 1080))
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
            numpy.copyto(windowArray, image)
        except IndexError:
            pass
        

        window.refresh()

        #timer.SDL_Delay(10)


    sdl2.ext.quit()
    return 0

if __name__ == "__main__":
    sys.exit(run())


