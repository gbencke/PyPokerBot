"""
This module contains functions to scan the Windows Operating System for Windows Handles (HWND).
"""
import win32gui


def scan_windows(hwnd_parent=0):
    """
    Returns a list of dictionaries containing the windows found on the windows desktop GUI.

    :param hwnd_parent: The parent HWND, starts with 0 (root window)
    :return: A list of dictionaries containing: hwnd, title, class and its parent
    """
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

