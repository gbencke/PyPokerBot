"""
This module contains several functions to handle screenshots that are taken from the
Poker Client GUIs.
"""
from ctypes import windll, c_char_p, c_buffer
from struct import calcsize, pack
from PIL import Image
import win32gui

# Win32 constants
NULL = 0
HORZRES = 8
VERTRES = 10
SRCCOPY = 13369376
HGDI_ERROR = 4294967295
ERROR_INVALID_PARAMETER = 87


def grab_screen(bbox=None):
    """
    This function returns a image of the entire computer desktop screen
    """

    def cleanup():
        """
        cleanup the windows handle of the bitmap object
        :return: None
        """
        if bitmap:
            windll.gdi32.DeleteObject(bitmap)
        windll.gdi32.DeleteDC(screen_copy)
        windll.gdi32.DeleteDC(screen)

    try:
        screen = windll.gdi32.CreateDC(c_char_p('DISPLAY'), NULL, NULL, NULL)
        screen_copy = windll.gdi32.CreateCompatibleDC(screen)

        if bbox:
            left, top, current_x2, current_y2 = bbox
            width = current_x2 - left + 1
            height = current_y2 - top + 1
        else:
            left = 0
            top = 0
            width = windll.gdi32.GetDeviceCaps(screen, HORZRES)
            height = windll.gdi32.GetDeviceCaps(screen, VERTRES)

        bitmap = windll.gdi32.CreateCompatibleBitmap(screen, width, height)
        if bitmap == NULL:
            print 'grab_screen: Error calling CreateCompatibleBitmap. Returned NULL'
            return

        hobj = windll.gdi32.SelectObject(screen_copy, bitmap)
        if hobj == NULL or hobj == HGDI_ERROR:
            print 'grab_screen: Error calling SelectObject. Returned {0}.'.format(hobj)
            return

        if windll.gdi32.BitBlt \
                    (screen_copy,
                     0,
                     0,
                     width,
                     height,
                     screen,
                     left,
                     top,
                     SRCCOPY) == NULL:
            print 'grab_screen: Error calling BitBlt. Returned NULL.'
            return

        bitmap_header = pack('LHHHH', calcsize('LHHHH'), width, height, 1, 24)
        bitmap_buffer = c_buffer(bitmap_header)
        bitmap_bits = c_buffer(' ' * (height * ((width * 3 + 3) & -4)))
        got_bits = windll.gdi32.GetDIBits(
            screen_copy, bitmap, 0, height, bitmap_bits, bitmap_buffer, 0)
        if got_bits == NULL or got_bits == ERROR_INVALID_PARAMETER:
            print 'grab_screen: Error calling GetDIBits. Returned {0}.'.format(got_bits)
            return

        image = Image.frombuffer(
            'RGB',
            (width, height),
            bitmap_bits,
            'raw',
            'BGR',
            (width * 3 + 3) & -4, -1)
        return image
    finally:
        cleanup()


def capture_screenshot(hwnd, file_to_save, should_save=True):
    """
    This is the main function for this module, as it receives as parameter the HWND
    (Windows Handle) identifying the correct screen to capture, and if specified, the
    file_name where we need to save that screen shot.

    :param hwnd: The HWND (Windows Handle) for that Window.
    :param file_to_save: The name of the file to save the image
    :param should_save: Should we save the image?
    :return: Return a numpy array containing a image
    """
    if not hwnd == win32gui.GetForegroundWindow():
        win32gui.SetForegroundWindow(hwnd)
    win32gui.MoveWindow(hwnd, 0, 0, 1042, 745, True)
    rect = win32gui.GetWindowRect(hwnd)
    image_to_analyse = grab_screen()
    image_to_analyse = image_to_analyse.crop((rect[0], rect[1], rect[2], rect[3]))
    image_to_analyse = image_to_analyse.resize((int(1303), int(931)), Image.ANTIALIAS)
    if should_save:
        image_to_analyse.save(file_to_save)
    return image_to_analyse


