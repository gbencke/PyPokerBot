"""
This module contains very simple Win32 functions to check for certain windows status
"""
import win32gui


def is_window_with_focus(hwnd):
    """
    Check if a certain window (identified by its HWND) has focus or not.

    :param hwnd: The Windows Handle (HWND) which identifies it on Windows OS.
    :return: True or False
    """
    return win32gui.GetForegroundWindow() == hwnd


def is_minimized(hwnd):
    """
    Check if a certain window (identified by its HWND) is minimized or not.

    :param hwnd: The Windows Handle (HWND) which identifies it on Windows OS.
    :return: True or False
    """
    return win32gui.IsIconic(hwnd)
