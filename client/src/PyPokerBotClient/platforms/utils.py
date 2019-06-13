"""
This module contains several utility functions that are shared among all possible
poker cliente platforms. They mainly deal with data and image manipulation
"""
import numpy
from cv2 import calcHist, normalize

from PyPokerBotClient.osinterface.image import grab_image_from_file
from PyPokerBotClient.settings import GLOBAL_SETTINGS as Settings


def get_histogram_from_image(image):
    """
    From a Numpy array loaded using a Image manipulation toolkit like
    skimage or PIL, creates a histogram, a flattened vector of all the
    color values of the image in order to compare it.

    :param image: Numpy Array containing the image
    :return: A Flattened histogram of the image
    """
    image_cv2 = numpy.array(image)[:, :, ::-1].copy()
    image_cv2_hist = calcHist([image_cv2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    dst = image_cv2_hist.copy()
    return normalize(image_cv2_hist, dst).flatten()


def create_list_seats(number_of_seats):
    """
    Utility function to create a array of empty seats as None
    :param NumberOfSeats: Number of Seats (itens on the list)
    :return: List of None entities in a range of NumberOfSeats
    """
    return [None for _ in range(number_of_seats)]


def create_list_boolean_seats(number_of_seats):
    """
    Utility function to create a array of empty seats as boolean
    :param NumberOfSeats: Number of Seats (itens on the list)
    :return: List of False Value entities in a range of NumberOfSeats
    """
    return [False] * number_of_seats


def create_list_string_seats(number_of_seats):
    """
    Utility function to create a array of empty seats as empty strings
    :param NumberOfSeats: Number of Seats (itens on the list)
    :return: List of empty strings in a range of NumberOfSeats
    """
    return [''] * number_of_seats


def get_suite_from_image(selected_image):
    """
    From a certain image, try to determine its suite ( clubs, spades,
    diamonds or hearts). It uses a algorithm to check the predominant
    colocar on the image and then check the corresponding suit.

    :param selected_image: Numpy Array containing a image
    :return: 'c' for clubs, 's' for spades,
             'h' for hearts, 'd' for diamonds
    """
    red = 0
    blue = 0
    green = 0
    black = 0
    for current_w in range(selected_image.width):
        for current_h in range(selected_image.height):
            pixel = selected_image.getpixel((current_w, current_h))
            if pixel[0] >= 230 and pixel[1] >= 230 and pixel[2] >= 230:
                continue
            if pixel[0] < 20 and pixel[1] < 20 and pixel[2] < 20:
                black += 1
                continue
            if pixel[0] >= pixel[1] and pixel[0] >= pixel[2]:
                red += 1
                continue
            if pixel[1] >= pixel[0] and pixel[1] >= pixel[2]:
                green += 1
                continue
            if pixel[2] >= pixel[0] and pixel[2] >= pixel[1]:
                blue += 1
                continue
    if black > 200:
        return 's'
    if red > green and red > blue and red > black:
        return 'h'
    if green > red and green > blue and green > black:
        return 'c'
    if blue > red and blue > green and blue > black:
        return 'd'


def get_card_template(platform, current_card, current_suit):
    """
    This utility function returns the Numpy array containing the
    image of a certain card and suit.

    :param Platform: The current Poker Platform (888, PokerStarts)
    :param current_card: A string containing the card value (2-9,T,J,Q,K,A)
    :param current_suit: The index of the seat to be returned (h,c,s,d)
    :return: A numpy array containing the image to be returned
    """
    filename = Settings.get_card_template(platform, current_card, current_suit)
    image_template = grab_image_from_file(filename)
    return numpy.array(image_template)[:, :, ::-1].copy()
