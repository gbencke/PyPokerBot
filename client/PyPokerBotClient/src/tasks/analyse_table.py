import numpy
import cv2
import os
from settings import settings
from helpers.win32.screenshot import grab_image_from_file, grab_image_pos_from_image


def get_histogram_from_image(Image):
    image_cv2 = numpy.array(Image)[:, :, ::-1].copy()
    image_cv2_hist = cv2.calcHist([image_cv2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    dst = image_cv2_hist.copy()
    return cv2.normalize(image_cv2_hist, dst).flatten()


def analyse_players_with_cards(Image):
    template_has_card_cv2_hist = get_histogram_from_image(
        grab_image_from_file(settings['TABLE_SCANNER']['PLAYERCARD_HAS_UNKNOWN_CARD_TEMPLATE']))
    for current_seat_index in range(6):
        current_seat_cv2_hist = get_histogram_from_image(grab_image_pos_from_image(
            Image, settings['TABLE_SCANNER']['PLAYER{}_HASCARD'.format(current_seat_index + 1)],
            settings['TABLE_SCANNER']['PLAYERHASCARD_SIZE']))
        print "For method {} seat {}:{}".format('Histogram', current_seat_index + 1,
                                                'Sentado' if cv2.compareHist(
                                                    template_has_card_cv2_hist,
                                                    current_seat_cv2_hist, 0) > settings['TABLE_SCANNER'][
                                                                 'PLAY_HASCARD_THRESHOLD'] else 'Vago')


def analyse_button(Image):
    template_has_card_cv2_hist = get_histogram_from_image(
        grab_image_from_file(settings['TABLE_SCANNER']['BUTTON_TEMPLATE']))
    for current_seat_index in range(6):
        current_seat_cv2_hist = get_histogram_from_image(grab_image_pos_from_image(
            Image, settings['TABLE_SCANNER']['BUTTON{}'.format(current_seat_index + 1)],
            settings['TABLE_SCANNER']['BUTTON_SIZE']))
        res = cv2.compareHist(template_has_card_cv2_hist, current_seat_cv2_hist, 0)
        print "For method {} button pos {}:{}".format('Histogram', current_seat_index + 1,
                                                      'BUTTON' if res > settings['TABLE_SCANNER'][
                                                          'BUTTON_THRESHOLD'] else '')


def analyse_flop_hist(Image):
    for current_flop_pos in range(5):
        selected_card = ''
        selected_card_res = 0
        current_flop_hst = get_histogram_from_image(grab_image_pos_from_image(
            Image,
            settings['TABLE_SCANNER']['FLOPCARD{}'.format(current_flop_pos + 1)],
            settings['TABLE_SCANNER']['FLOPCARD_SIZE']))
        for current_suit in ['h', 's', 'c', 'd']:
            for current_card in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']:
                filename = settings['TABLE_SCANNER']['TEMPLATES_FOLDER'] + '\\' + current_card + current_suit + '.jpg'
                current_card_image_hst = get_histogram_from_image(grab_image_from_file(filename))
                res = cv2.compareHist(current_flop_hst, current_card_image_hst, 2)
                if res > selected_card_res:
                    selected_card = current_card + current_suit
                    selected_card_res = res
                print("For FLOP{}, Card {} returned {} - WINNER {} ".format(current_flop_pos + 1, current_card + current_suit, res, selected_card))


def analyse_flop_template(Image):
    for current_flop_pos in range(5):
        selected_card = ''
        selected_card_res = 1000000
        current_flop_image = \
            numpy.array(
                grab_image_pos_from_image(
                    Image,
                    settings['TABLE_SCANNER']['FLOPCARD{}'.format(current_flop_pos + 1)],
                    settings['TABLE_SCANNER']['FLOPCARD_SIZE']))[:, :, ::-1].copy()
        for current_suit in ['h', 's', 'c', 'd']:
            for current_card in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']:
                filename = settings['TABLE_SCANNER']['TEMPLATES_FOLDER'] + '\\' + current_card + current_suit + '.jpg'
                current_card_image = numpy.array(grab_image_from_file(filename))[:, :, ::-1].copy()
                res = cv2.matchTemplate(current_flop_image, current_card_image, 0)
                if res < selected_card_res:
                    selected_card = current_card + current_suit
                    selected_card_res = res
                print("For FLOP{}, Card {} returned {} - WINNER {} ".format(current_flop_pos + 1, current_card + current_suit, res, selected_card))

def execute(args):
    if len(args) < 1:
        print("For this task you need at least 1 arguments: <Image Source> ")
        return
    image_name = args[0]
    im = grab_image_from_file(image_name)
    analyse_players_with_cards(im)
    analyse_button(im)
    #analyse_flop_hist(im)
    analyse_flop_template(im)
