import logging
import pyscreenshot as ImageGrab


def capture_screenshot(hwnd, file_to_save):
    logging.debug("Capturing {} to {}".format(hwnd, file_to_save))
    im = ImageGrab.grab()
    im.show()
