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

        rpi_name, jpg_buffer = image_hub.recv_jpg()
        print("got image")
        image = simplejpeg.decode_jpeg( jpg_buffer, colorspace='GRAY')
        windowArray[:,:,0:3] = image.swapaxes(0,1)
        #repeated = numpy.repeat(image, 4, axis=2)
        #numpy.copyto(windowArray, repeated)

        window.refresh()
        image_hub.send_reply(b'OK')

        #timer.SDL_Delay(10)


    sdl2.ext.quit()
    return 0

if __name__ == "__main__":
    sys.exit(run())


