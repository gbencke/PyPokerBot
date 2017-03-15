import logging
import pyscreenshot as ImageGrab
import win32gui


def capture_screenshot(hwnd, file_to_save):
    logging.debug("Capturing {} to {}".format(hwnd, file_to_save))
    try:
        win32gui.SetForegroundWindow(hwnd)
        rect = win32gui.GetWindowRect(hwnd)
        im = ImageGrab.grab()
        im = im.crop((rect[0] * 1.25, rect[1] * 1.25, rect[2] * 1.25, rect[3] * 1.25))
        im.save(file_to_save)
    except Exception as e:
        logging.debug('Error:' + str(e))
