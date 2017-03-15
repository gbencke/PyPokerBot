from datetime import datetime


class PokerTable:
    def __init__(self, hwnd, name, stakes, format):
        self.hwnd = hwnd
        self.name = name
        self.stakes = stakes
        self.format = format

    def get_screenshot_name(self):
        return 'Screenshot.' + datetime.now().strftime("%Y%m%d%H%M%S.%f") + "." + self.name + ".Table.jpg"
