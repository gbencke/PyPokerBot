# coding=utf-8
"""
This modules has all the custom exceptions that are specific to the PyPokerBot Client
"""
class NeedToSpecifySeatsException(Exception):
    """
    This exception is raised when we dont specify the correct number of seats in a table
    """
    def __init__(self, message):
        super(Exception, self).__init__(message)


class MoreThanOneLobbyPerPlatformException(Exception):
    """
    It is not possible to have more than one lobby per poker platform
    """
    def __init__(self, message):
        super(Exception, self).__init__(message)


class NeedToSpecifyTableTypeException(Exception):
    """
    This exception is raised when we dont specify the correct table type for a table
    """
    def __init__(self, message):
        super(Exception, self).__init__(message)
