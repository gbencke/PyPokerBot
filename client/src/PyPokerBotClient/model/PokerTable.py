"""
This module contains a abstract class representing a Poker table.
"""
from datetime import datetime


class PokerTable(object):
    """
    Abstract class representing a poker table from a certain platform.
    """
    def __init__(self, hwnd, name, stakes, format, scanner, strategy, lobby):
        """
        Default constructor

        :param hwnd: Windows HWND identifying the table.
        :param name: The name of the table
        :param stakes: The Stakes (Bet Amount)
        :param format: If it is 6-SEAT, 9-SEAT, OMAHA or other
        :param scanner: The PokerTableScanner class to be used
        :param strategy: The PokerStrategy class to use
        :param lobby: The parent PokerLobby instance class
        """
        self.hwnd = hwnd
        self.name = name
        self.stakes = stakes
        self.format = format
        self.scanner = scanner
        self.strategy = strategy
        self.lobby = lobby
        self.table_scans = []

    def get_screenshot_name(self):
        """
        Returns a string containing a suggested filename for the current table screenshot

        :return: string containing a suggested filename for the current table screenshot
        """
        return 'Screenshot.' + datetime.now().strftime("%Y%m%d%H%M%S.%f") + "." + self.name + ".Table.jpg"

    def refresh_from_image(self, image):
        """
        Refresh the current playing table image.

        :param image: Last image taken
        :return: A numpy array representing the current table.
        """
        self.table_scans.append(self.scanner.analyze_from_image(image))
        return self.table_scans[-1]

    def generate_decision(self, analisys):
        """
        This method returns the decision to be made by the PokerBot based on
        the analisys dictionary returned by the PokerTableScanner instance

        :param analisys: The analisys dictionary returned by a PokerTableScanner instance
        :return: A tuple containing the decision: RAISE OR CALL, CALL OR FOLD, FOLD OR CHECK
            and the amount in big blinds to raise or call.
        """
        return self.strategy.run_strategy(analisys)

    def has_command_to_execute(self, analisys):
        """
        Verifies on the analisys dictionary if the Poker Client UI is expecting a decision
        to be made, and a command to be send.

        :param analisys: The analisys dictionary returned by a PokerTableScanner instance
        :return: True or False
        """
        return self.scanner.has_command_to_execute(analisys)
