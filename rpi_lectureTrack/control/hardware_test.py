import logging
import math
import time

from picamera import PiCamera


# https://github.com/pimoroni/pantilt-hat/blob/master/examples/smooth.py


def camera_test(rotation):
    camera = PiCamera()
    camera.rotation = rotation
    logging.info('Starting Raspberry Pi Camera')
    camera.start_preview()

    try:
        while True:
            continue
    except KeyboardInterrupt:
        logging.info('Stopping Raspberry Pi Camera')
        camera.stop_preview()


def pantilt_test():
    logging.info('Starting Pan-Tilt HAT test!')
    logging.info('Pan-Tilt HAT should follow a smooth sine wave')


if __name__ == '__main__':
    pantilt_test()
