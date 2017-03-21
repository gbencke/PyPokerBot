import win32gui
import pyautogui

import logging
from settings import settings


def scan_windows(hwnd_parent=0):
    ret = []
    current_hwnd = 0
    while True:
        current_hwnd = win32gui.FindWindowEx(hwnd_parent, current_hwnd, None, None)
        if current_hwnd == 0:
            break
        else:
            window_title = win32gui.GetWindowText(current_hwnd)
            window_class = win32gui.GetClassName(current_hwnd)
            new_hwnd = {"hwnd": current_hwnd, "title": window_title, "class": window_class, "parent": hwnd_parent}
            ret.append(new_hwnd)
            scan_windows(current_hwnd)
    return ret


def run_command(hwnd, button_to_press):
    if button_to_press == 0:
        button_to_press = 1
    if button_to_press not in [1,2,3]:
        return
    x = int((settings['TABLE_SCANNER']['COMMAND_POS{}'.format(button_to_press)][0]+20)/1.25)
    y = int((settings['TABLE_SCANNER']['COMMAND_POS{}'.format(button_to_press)][1]+20)/1.25)
    logging.debug('Click on button {}, pos ({},{})'.format(button_to_press, x, y))
    win32gui.SetForegroundWindow(hwnd)
    pyautogui.click(x, y)
    return
