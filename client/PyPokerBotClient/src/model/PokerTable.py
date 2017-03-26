from datetime import datetime


class PokerTable:
    def __init__(self, hwnd, name, stakes, format, scanner, strategy, lobby):
        self.hwnd = hwnd
        self.name = name
        self.stakes = stakes
        self.format = format
        self.scanner = scanner
        self.strategy = strategy
        self.lobby = lobby

    def get_screenshot_name(self):
        return 'Screenshot.' + datetime.now().strftime("%Y%m%d%H%M%S.%f") + "." + self.name + ".Table.jpg"

    def refresh_from_image(self):
        pass

    def generate_decision(self):
        pass

