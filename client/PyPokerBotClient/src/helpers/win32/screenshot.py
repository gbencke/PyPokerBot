import logging
import pyscreenshot as ImageGrab
import win32gui
import PIL


def capture_screenshot(hwnd, file_to_save):
    logging.debug("Capturing {} to {}".format(hwnd, file_to_save))
    try:
        win32gui.SetForegroundWindow(hwnd)
        win32gui.MoveWindow(hwnd, 0, 0, 1042, 745, True)
        rect = win32gui.GetWindowRect(hwnd)
        #print rect
        #exit(0)
        im = ImageGrab.grab()
        im = im.crop((rect[0] * 1.25, rect[1] * 1.25, rect[2] * 1.25, rect[3] * 1.25))
        im.save(file_to_save)
        return im
    except Exception as e:
        logging.debug('Error:' + str(e))
        return None


def grab_image_from_file(image):
    return PIL.Image.open(image)


def grab_image_pos_from_image(image, pos, size):
    return image.crop((pos[0], pos[1], pos[0] + size[0], pos[1] + size[1]))


def grab_image_pos_from_file(file_name, pos, size):
    im = PIL.Image.open(file_name)
    return grab_image_pos_from_image(im, pos, size)
