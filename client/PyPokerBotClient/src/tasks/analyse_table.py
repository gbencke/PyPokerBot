import numpy
import cv2
import pprint
from settings import settings
from helpers.win32.screenshot import grab_image_from_file, grab_image_pos_from_image


def get_histogram_from_image(Image):
    image_cv2 = numpy.array(Image)[:, :, ::-1].copy()
    image_cv2_hist = cv2.calcHist([image_cv2], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    dst = image_cv2_hist.copy()
    return cv2.normalize(image_cv2_hist, dst).flatten()


def analyse_players_with_cards(Image):
    ret = {}
    template_has_card_cv2_hist = get_histogram_from_image(
        grab_image_from_file(settings['TABLE_SCANNER']['PLAYERCARD_HAS_UNKNOWN_CARD_TEMPLATE']))
    for current_seat_index in range(6):
        player_hascard_key = 'PLAYER{}_HASCARD'.format(current_seat_index + 1)
        current_seat_cv2_hist = get_histogram_from_image(grab_image_pos_from_image(
            Image, settings['TABLE_SCANNER'][player_hascard_key],
            settings['TABLE_SCANNER']['PLAYERHASCARD_SIZE']))
        ret[player_hascard_key] = 'CARD' if cv2.compareHist(
            template_has_card_cv2_hist,
            current_seat_cv2_hist, 0) > settings['TABLE_SCANNER'][
                                                'PLAY_HASCARD_THRESHOLD'] else ''
        # print "For method {} seat {}:{}".format('Histogram', current_seat_index + 1, ret[player_hascard_key])
    return ret


def analyse_players_without_cards(Image):
    ret = {}
    for current_seat_index in range(6):
        empty_card_key = settings['TABLE_SCANNER']['TEMPLATES_FOLDER'] + '\\' + 'PLAYER{}_HASNOCARD'.format(
            current_seat_index + 1) + '.jpg'
        empty_card_hst = get_histogram_from_image(grab_image_from_file(empty_card_key))
        current_pos_key = 'PLAYER{}_HASCARD'.format(current_seat_index + 1)
        current_pos_hst = get_histogram_from_image(grab_image_pos_from_image(
            Image, settings['TABLE_SCANNER'][current_pos_key],
            settings['TABLE_SCANNER']['PLAYERHASCARD_SIZE']))
        res = cv2.compareHist(empty_card_hst, current_pos_hst, 0)
        ret['NOCARD{}'.format(current_seat_index + 1)] = 'NOCARD' if res > settings['TABLE_SCANNER'][
            'PLAY_HASCARD_THRESHOLD'] else ''
    return ret


def analyse_button(Image):
    ret = {}
    template_has_card_cv2_hist = get_histogram_from_image(
        grab_image_from_file(settings['TABLE_SCANNER']['BUTTON_TEMPLATE']))
    for current_seat_index in range(6):
        button_name_key = 'BUTTON{}'.format(current_seat_index + 1)
        current_seat_cv2_hist = get_histogram_from_image(grab_image_pos_from_image(
            Image, settings['TABLE_SCANNER'][button_name_key],
            settings['TABLE_SCANNER']['BUTTON_SIZE']))
        res = cv2.compareHist(template_has_card_cv2_hist, current_seat_cv2_hist, 0)
        ret[button_name_key] = 'BUTTON' if res > settings['TABLE_SCANNER']['BUTTON_THRESHOLD'] else ''
        # print "For method {} button pos {}:{}".format('Histogram', current_seat_index + 1, ret[button_name_key])
    return ret


def analyse_flop_template(Image):
    ret = {}
    template_flop_empty_cv2_hist = get_histogram_from_image(
        grab_image_from_file(settings['TABLE_SCANNER']['FLOPCARD_HAS_NOCARD_TEMPLATE']))
    template_flop_pos1 = \
        get_histogram_from_image(grab_image_pos_from_image(
            Image,
            settings['TABLE_SCANNER']['FLOPCARD1'],
            settings['TABLE_SCANNER']['FLOPCARD_SIZE']))
    res = cv2.compareHist(template_flop_empty_cv2_hist, template_flop_pos1, 0)
    if res > settings['TABLE_SCANNER']['PLAY_HASCARD_THRESHOLD']:
        return ret
    for current_flop_pos in range(5):
        selected_card = ''
        selected_card_res = 1000000
        flop_card_key = 'FLOPCARD{}'.format(current_flop_pos + 1)
        current_flop_image = \
            numpy.array(
                grab_image_pos_from_image(
                    Image,
                    settings['TABLE_SCANNER'][flop_card_key],
                    settings['TABLE_SCANNER']['FLOPCARD_SIZE']))[:, :, ::-1].copy()
        for current_suit in ['h', 's', 'c', 'd']:
            for current_card in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']:
                filename = settings['TABLE_SCANNER']['TEMPLATES_FOLDER'] + '\\' + current_card + current_suit + '.jpg'
                current_card_image = numpy.array(grab_image_from_file(filename))[:, :, ::-1].copy()
                res = cv2.matchTemplate(current_flop_image, current_card_image, 0)
                if res < selected_card_res:
                    selected_card = current_card + current_suit
                    selected_card_res = res
                    # print("For FLOP{}, Card {} returned {} - WINNER {} ".format(current_flop_pos + 1,current_card + current_suit,res, selected_card))
        ret[flop_card_key] = selected_card
    return ret


def analyse_hero(im, cards, nocards):
    ret = {}
    ret['HERO_CARDS'] = ''
    for seat in range(6):
        card_key = 'PLAYER{}_HASCARD'.format(seat + 1)
        nocard_key = 'NOCARD{}'.format(seat + 1)
        if len(cards[card_key]) == 0 and len(nocards[nocard_key]) == 0:
            #print("found hero at {}".format(seat + 1))
            ret['HERO_POS'] = seat + 1
            for current_hero_card in range(2):
                selected_card = ''
                selected_card_res = 1000000
                flop_card_key = 'PLAYERCARD{}{}_POS'.format(seat + 1, current_hero_card + 1)
                current_flop_image = \
                    numpy.array(
                        grab_image_pos_from_image(
                            im,
                            settings['TABLE_SCANNER'][flop_card_key],
                            settings['TABLE_SCANNER']['FLOPCARD_SIZE']))[:, :, ::-1].copy()
                for current_suit in ['h', 's', 'c', 'd']:
                    for current_card in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']:
                        filename = settings['TABLE_SCANNER'][
                                       'TEMPLATES_FOLDER'] + '\\' + current_card + current_suit + '.jpg'
                        current_card_image = numpy.array(grab_image_from_file(filename))[:, :, ::-1].copy()
                        res = cv2.matchTemplate(current_flop_image, current_card_image, 0)
                        #print('filename:{} res:{}'.format(filename, res))
                        if res < selected_card_res:
                            selected_card = current_card + current_suit
                            selected_card_res = res
                ret['HERO_CARDS'] += selected_card
    return ret


def execute(args):
    if len(args) < 1:
        print("For this task you need at least 1 arguments: <Image Source> ")
        return
    image_name = args[0]
    im = grab_image_from_file(image_name)

    result = {}
    result['cards'] = analyse_players_with_cards(im)
    result['nocards'] = analyse_players_without_cards(im)
    result['hero'] = analyse_hero(im, result['cards'], result['nocards'])
    result['button'] = analyse_button(im)
    result['flop'] = analyse_flop_template(im)
    pprint.PrettyPrinter().pprint(result)
