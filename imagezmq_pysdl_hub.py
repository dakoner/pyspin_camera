#!/usr/bin/python3
# run this program on the Mac to display image streams from multiple RPis
import numpy
import sys
import sdl2
import sdl2.ext
import imagezmq
import simplejpeg
from sdl2 import events
import ctypes


def run():
    image_hub = imagezmq.ImageHub()

    sdl2.ext.init()
    window = sdl2.ext.Window("Hello World!", size=(1080,1440))
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
        window.refresh()

        rpi_name, jpg_buffer = image_hub.recv_jpg()
        image = simplejpeg.decode_jpeg( jpg_buffer, colorspace='GRAY')
        image_hub.send_reply(b'OK')
        print("copy")

        repeated = numpy.repeat(image, 4, axis=2)
        print(repeated.shape)
        numpy.copyto(windowArray, repeated)
        window.refresh()
        #timer.SDL_Delay(10)


    sdl2.ext.quit()
    return 0

if __name__ == "__main__":
    sys.exit(run())


