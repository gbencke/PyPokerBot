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
        self.table_scans = []

    def get_screenshot_name(self):
        return 'Screenshot.' + datetime.now().strftime("%Y%m%d%H%M%S.%f") + "." + self.name + ".Table.jpg"

    def refresh_from_image(self, image):
        self.table_scans.append(self.scanner.analyze_from_image(image))
        return self.table_scans[-1]

    def generate_decision(self, analisys):
        return self.strategy.run_strategy(analisys)

    def has_command_to_execute(self, analisys):
        return self.strategy.has_command_to_execute(analisys)
