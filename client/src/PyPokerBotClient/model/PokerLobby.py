"""
This module contains a abstract class that represents a PokerLobby
"""


class PokerLobby(object):
    """
    Abstract Class that represents a PokerLobby
    """

    def __init__(self):
        """
        Default Constructor
        """
        pass

    @staticmethod
    def usage():
        """
        Show a simple description of this instance
        :return: None
        """
        print "Main PokerLobby Class, needs to be specialized according to platform"

    def __str__(self):
        """
        toString() implementation
        :return: None
        """
        return self.usage()

    def __repr__(self):
        """
        Representation() implementation
        :return: None
        """
        return self.usage()
