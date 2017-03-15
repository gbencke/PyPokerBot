import settings
import helpers.win32.helper as win32


def scan_for_lobbys():
    windows_found = win32.scan_windows()
