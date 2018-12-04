import win32gui


def is_window_with_focus(hwnd):
    return win32gui.GetForegroundWindow() == hwnd


def is_minimized(hwnd):
    return win32gui.IsIconic(hwnd)
