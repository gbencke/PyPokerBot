import numpy
import cv2
from PyPokerBotClient.osinterface.win32.screenshot import grab_image_from_file, grab_image_pos_from_image
from PyPokerBotClient.settings import GlobalSettings as Settings


def get_histogram_from_image(image):
    image_cv2 = numpy.array(image)[:, :, ::-1].copy()
    image_cv2_hist = cv2.calcHist([image_cv2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    dst = image_cv2_hist.copy()
    return cv2.normalize(image_cv2_hist, dst).flatten()


def create_list_none_with_number_seats(NumberOfSeats):
    return [None for _ in range(NumberOfSeats)]


def create_list_boolean_with_number_seats(NumberOfSeats):
    return [False] * NumberOfSeats


def create_list_string_with_number_seats(NumberOfSeats):
    return [''] * NumberOfSeats


def get_suite_from_image(selected_image):
    red = 0
    blue = 0
    green = 0
    black = 0
    for w in range(selected_image.width):
        for h in range(selected_image.height):
            pixel = selected_image.getpixel((w, h))
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


def get_card_template(Platform, current_card, current_suit):
    filename = Settings.get_card_template(Platform, current_card, current_suit)
    Image_template = grab_image_from_file(filename)
    return Image_template, numpy.array(Image_template)[:, :, ::-1].copy()
