"""
This module contains several functions to handle screenshots that are taken from the
Poker Client GUIs.
"""
import win32gui
from PIL import Image
from ctypes import windll, c_char_p, c_buffer
from struct import calcsize, pack

gdi32 = windll.gdi32

# Win32 functions
CreateDC = gdi32.CreateDCA
CreateCompatibleDC = gdi32.CreateCompatibleDC
GetDeviceCaps = gdi32.GetDeviceCaps
CreateCompatibleBitmap = gdi32.CreateCompatibleBitmap
BitBlt = gdi32.BitBlt
SelectObject = gdi32.SelectObject
GetDIBits = gdi32.GetDIBits
DeleteDC = gdi32.DeleteDC
DeleteObject = gdi32.DeleteObject

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
        if bitmap:
            DeleteObject(bitmap)
        DeleteDC(screen_copy)
        DeleteDC(screen)

    try:
        screen = CreateDC(c_char_p('DISPLAY'), NULL, NULL, NULL)
        screen_copy = CreateCompatibleDC(screen)

        if bbox:
            left, top, x2, y2 = bbox
            width = x2 - left + 1
            height = y2 - top + 1
        else:
            left = 0
            top = 0
            width = GetDeviceCaps(screen, HORZRES)
            height = GetDeviceCaps(screen, VERTRES)

        bitmap = CreateCompatibleBitmap(screen, width, height)
        if bitmap == NULL:
            print('grab_screen: Error calling CreateCompatibleBitmap. Returned NULL')
            return

        hobj = SelectObject(screen_copy, bitmap)
        if hobj == NULL or hobj == HGDI_ERROR:
            print('grab_screen: Error calling SelectObject. Returned {0}.'.format(hobj))
            return

        if BitBlt(screen_copy, 0, 0, width, height, screen, left, top, SRCCOPY) == NULL:
            print('grab_screen: Error calling BitBlt. Returned NULL.')
            return

        bitmap_header = pack('LHHHH', calcsize('LHHHH'), width, height, 1, 24)
        bitmap_buffer = c_buffer(bitmap_header)
        bitmap_bits = c_buffer(' ' * (height * ((width * 3 + 3) & -4)))
        got_bits = GetDIBits(screen_copy, bitmap, 0, height, bitmap_bits, bitmap_buffer, 0)
        if got_bits == NULL or got_bits == ERROR_INVALID_PARAMETER:
            print('grab_screen: Error calling GetDIBits. Returned {0}.'.format(got_bits))
            return

        image = Image.frombuffer('RGB', (width, height), bitmap_bits, 'raw', 'BGR', (width * 3 + 3) & -4, -1)
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
    im = grab_screen()
    im = im.crop((rect[0], rect[1], rect[2], rect[3]))
    im = im.resize((int(1303), int(931)), Image.ANTIALIAS)
    if should_save:
        im.save(file_to_save)
    return im


def grab_image_from_file(image):
    """
    Loads a certain image from a filename and returns a numpy array representing it.

    :param image: The filename to load.
    :return: The numpy array representing the image
    """
    return Image.open(image)


def grab_image_pos_from_image(image, pos, size):
    """
    Returns a region of the image based on a certain position and size.

    :param image: The numpy array representing the image
    :param pos: The Top-Left position
    :param size: The size of the image
    :return: A numpy array of the region, representing the image.
    """
    return image.crop((pos[0], pos[1], pos[0] + size[0], pos[1] + size[1]))


def grab_image_pos_from_file(file_name, pos, size):
    """
    Returns a region of the image in the file name specified, based on a certain position and size

    :param file_name: The file name of the image
    :param pos: The Top-Left position
    :param size: The size of the image
    :return: A numpy array of the region, representing the image.
    """
    im = Image.open(file_name)
    return grab_image_pos_from_image(im, pos, size)
