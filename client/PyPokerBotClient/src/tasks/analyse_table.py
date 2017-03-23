import ast
import numpy
import cv2
import pprint
import subprocess
import requests
import os
import logging
from datetime import datetime
from time import sleep
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

    for current_seat_index in range(6):
        empty_card_key = settings['TABLE_SCANNER']['TEMPLATES_FOLDER'] + '\\' + 'BUTTON{}_TEMPLATE'.format(
            current_seat_index + 1) + '.jpg'
        template_has_card_cv2_hist = get_histogram_from_image(grab_image_from_file(empty_card_key))
        button_name_key = 'BUTTON{}'.format(current_seat_index + 1)
        current_seat_cv2_hist = get_histogram_from_image(grab_image_pos_from_image(
            Image, settings['TABLE_SCANNER'][button_name_key],
            settings['TABLE_SCANNER']['BUTTON_SIZE']))
        res = cv2.compareHist(template_has_card_cv2_hist, current_seat_cv2_hist, 0)
        ret[button_name_key] = 'BUTTON' if res > settings['TABLE_SCANNER']['BUTTON_THRESHOLD'] else ''
        # logging.debug("For method {} button pos {}:{} {}".format('Histogram', current_seat_index + 1, ret[button_name_key], res))
    return ret


def analyse_flop_hist(Image):
    ret = {}
    for current_flop_pos in range(5):
        selected_card = ''
        selected_card_res = 0
        flop_card_key = 'FLOPCARD{}'.format(current_flop_pos + 1)
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
                    # print("For FLOP{}, Card {} returned {} - WINNER {} ".format(current_flop_pos + 1, current_card + current_suit, res, selected_card))
        ret[flop_card_key] = selected_card
    return ret


def analyse_flop_template(Image):
    ret = {}
    for current_flop_pos in range(5):
        template_flop_empty_cv2_hist = get_histogram_from_image(
            grab_image_from_file(settings['TABLE_SCANNER']['FLOPCARD_HAS_NOCARD_TEMPLATE']))
        template_flop_pos1 = \
            get_histogram_from_image(grab_image_pos_from_image(
                Image,
                settings['TABLE_SCANNER']['FLOPCARD{}'.format(current_flop_pos + 1)],
                settings['TABLE_SCANNER']['FLOPCARD_SIZE']))
        res = cv2.compareHist(template_flop_empty_cv2_hist, template_flop_pos1, 0)
        if res > settings['TABLE_SCANNER']['PLAY_HASCARD_THRESHOLD']:
            return ret
        selected_card = ''
        selected_card_res = 1000000000
        flop_card_key = 'FLOPCARD{}'.format(current_flop_pos + 1)
        image_from_flop_card = grab_image_pos_from_image(
            Image,
            settings['TABLE_SCANNER'][flop_card_key],
            settings['TABLE_SCANNER']['FLOPCARD_SIZE'])
        current_flop_image = numpy.array(image_from_flop_card)[:, :, ::-1].copy()
        for current_suit in ['h', 's', 'c', 'd']:
            for current_card in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']:
                filename = settings['TABLE_SCANNER']['TEMPLATES_FOLDER'] + '\\' + current_card + current_suit + '.jpg'
                current_card_image = numpy.array(grab_image_from_file(filename))[:, :, ::-1].copy()
                res = cv2.matchTemplate(current_flop_image, current_card_image, 0)
                # print("For FLOP{}, Card {} returned {} - WINNER {} ".format(current_flop_pos + 1, current_card + current_suit,res, selected_card))
                if res < selected_card_res:
                    selected_card = current_card + current_suit
                    selected_card_res = res
        correct_suit = get_suite_from_image(image_from_flop_card)
        if correct_suit != selected_card[1]:
            selected_card = selected_card[0] + correct_suit
        ret[flop_card_key] = selected_card
    return ret


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
    # print("red:{} green:{} blue:{} black:{}".format(red, green, blue, black))
    if black > 200:
        return 's'
    if red > green and red > blue and red > black:
        return 'h'
    if green > red and green > blue and green > black:
        return 'c'
    if blue > red and blue > green and blue > black:
        return 'd'


def get_hero_position(hero_pos, cards, button):
    if button['BUTTON{}'.format(hero_pos)] == 'BUTTON':
        return 'BUTTON'
    current_pos_analysed = hero_pos + 1
    while True:
        if current_pos_analysed > 6:
            current_pos_analysed = 1
        if cards['PLAYER{}_HASCARD'.format(current_pos_analysed)] == 'CARD':
            return ''
        if button['BUTTON{}'.format(current_pos_analysed)] == 'BUTTON':
            return 'BUTTON'
        current_pos_analysed += 1


def analyse_hero(im, cards, nocards, button):
    ret = {}
    ret['HERO_CARDS'] = ''
    for seat in range(6):
        card_key = 'PLAYER{}_HASCARD'.format(seat + 1)
        nocard_key = 'NOCARD{}'.format(seat + 1)
        if len(cards[card_key]) == 0 and len(nocards[nocard_key]) == 0:
            # print("found hero at {}".format(seat + 1))
            ret['HERO_POS'] = seat + 1
            for current_hero_card in range(2):
                selected_card = ''
                selected_card_res = 1000000000
                flop_card_key = 'PLAYERCARD{}{}_POS'.format(seat + 1, current_hero_card + 1)
                image_from_player = grab_image_pos_from_image(
                    im,
                    settings['TABLE_SCANNER'][flop_card_key],
                    settings['TABLE_SCANNER']['FLOPCARD_SIZE'])
                current_flop_image = numpy.array(image_from_player)[:, :, ::-1].copy()
                for current_suit in ['h', 's', 'c', 'd']:
                    for current_card in ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']:
                        filename = settings['TABLE_SCANNER'][
                                       'TEMPLATES_FOLDER'] + '\\' + current_card + current_suit + '.jpg'
                        image_from_file = grab_image_from_file(filename)
                        current_card_image = numpy.array(image_from_file)[:, :, ::-1].copy()
                        res = cv2.matchTemplate(current_flop_image, current_card_image, 0)
                        if res < selected_card_res:
                            selected_card = current_card + current_suit
                            selected_card_res = res
                correct_suit = get_suite_from_image(image_from_player)
                if correct_suit != selected_card[1]:
                    selected_card = selected_card[0] + correct_suit
                ret['HERO_CARDS'] += selected_card
            break
    hero_position = ''
    if 'HERO_POS' in ret:
        hero_position = get_hero_position(ret['HERO_POS'], cards, button)
    ret['POSITION'] = hero_position
    return ret


def analyse_commands(im):
    ret = {"COMMAND1": "", "COMMAND2": "", "COMMAND3": ""}

    for x in range(3):
        current_command = x + 1

        template_has_command_cv2_hist = get_histogram_from_image(
            grab_image_from_file(settings['TABLE_SCANNER']['COMMAND_TEST_TEMPLATE{}'.format(current_command)]))

        has_command_cv2_hist = \
            get_histogram_from_image(grab_image_pos_from_image(
                im,
                settings['TABLE_SCANNER']['COMMAND_POS{}'.format(current_command)],
                settings['TABLE_SCANNER']['COMMAND_TEST_SIZE']))
        res = cv2.compareHist(template_has_command_cv2_hist, has_command_cv2_hist, 0)
        if res > settings['TABLE_SCANNER']['COMMAND_TEST_TOLERANCE']:
            im_command = grab_image_pos_from_image(
                im,
                settings['TABLE_SCANNER']['COMMAND_POS{}'.format(current_command)],
                settings['TABLE_SCANNER']['COMMAND_SIZE']
            )
            command_image_name = 'command{}.jpg'.format(current_command)
            im_command.save(command_image_name)
            return_from_tesseract = subprocess.check_output(['tesseract', command_image_name, 'stdout'], shell=False)
            if len(return_from_tesseract.strip()) == 0:
                error_filename = command_image_name + '.error.' + datetime.now().strftime("%Y%m%d%H%M%S.%f") + '.jpg'
                logging.debug("ERROR ON TESSERACT!!! " + error_filename)
                im_command.save(error_filename)
            ret['COMMAND{}'.format(current_command)] = return_from_tesseract.replace('\r\n', ' ').replace('  ', ' ')
            os.remove(command_image_name)
            sleep(0.2)
    return ret


def analyse_hand(analisys):
    ret = {}
    if len(analisys['hero']['HERO_CARDS']) == 0:
        return ret

    total_villains = 0
    for x in range(analisys['seats']):
        current_seat = x + 1
        if analisys['cards']['PLAYER{}_HASCARD'.format(current_seat)] == 'CARD':
            total_villains += 1
    flop_cards = ''
    if len(analisys['flop'].keys()) > 0:
        for x in range(5):
            flop_card_key = 'FLOPCARD{}'.format(x + 1)
            if flop_card_key in analisys['flop']:
                flop_cards += analisys['flop'][flop_card_key]
    current_hand_phase = 'PREFLOP' if len(flop_cards) == 0 else 'FLOP'
    ret['HAND_PHASE'] = current_hand_phase
    card_strength = settings['STRATEGY'][current_hand_phase]['PLAYER_STRENGTH'] if len(flop_cards) == 0 else \
        settings['STRATEGY'][current_hand_phase]['PLAYER_STRENGTH']

    if current_hand_phase == 'PREFLOP' and total_villains > 2:
        total_villains = 2
    villains_cards = ":".join([card_strength for x in range(total_villains)])

    command_to_send = '{} {}'.format(analisys['hero']['HERO_CARDS'] + ':' + villains_cards, flop_cards)
    ret['COMMAND_TO_SEND'] = command_to_send
    logging.debug('Sent to server:' + command_to_send[:30])
    r = requests.post(settings['STRATEGY']['CALCULATE_URL'], json={"command": command_to_send})
    logging.debug('Received from server:' + str(r.content)[:30])
    if r.status_code == 200:
        ret['RESULT'] = ast.literal_eval(r.content)
    else:
        ret['RESULT'] = ''
    return ret


def get_confidence_level(analisys, phase):
    if phase == 'FLOP':
        return 'CONFIDENCE_LEVEL'

    total_villains = 0
    for x in range(analisys['seats']):
        current_seat = x + 1
        if analisys['cards']['PLAYER{}_HASCARD'.format(current_seat)] == 'CARD':
            total_villains += 1
    if total_villains == 1:
        return 'CONFIDENCE_LEVEL_HEADS_UP'
    else:
        if analisys['hero']['POSITION'] == 'BUTTON':
            return 'CONFIDENCE_LEVEL_POSITION'
        else:
            return 'CONFIDENCE_LEVEL'


def generate_decision_preflop(analisys):
    ret = {}
    phase = 'PREFLOP'

    confidence_level = settings['STRATEGY'][phase][get_confidence_level(analisys, phase)]
    confidence_level_raise = settings['STRATEGY'][phase]['CONFIDENCE_DIFFERENCE_RAISE']
    hand_equity = analisys['hand_analisys']['RESULT'][0][1]
    is_hero_in_button = (analisys['hero']['POSITION'] == 'BUTTON')

    logging.debug(
        'generate_decision_preflop({},{},{}) button:{}'.format(confidence_level, confidence_level_raise, hand_equity,
                                                               is_hero_in_button))

    ret['RAISE_STRATEGY'] = settings['STRATEGY']['FLOP']['RAISE_STRATEGY']
    if hand_equity >= (confidence_level + confidence_level_raise):
        ret['DECISION'] = 'RAISE'
        return ret
    if hand_equity >= (confidence_level):
        ret['DECISION'] = 'CALL'
        return ret
    else:
        ret['DECISION'] = 'FOLD OR CHECK'
    return ret


def verify_check_command(analisys):
    for x in range(3):
        if 'CHECK' in analisys['commands']['COMMAND{}'.format(x + 1)].upper():
            return True
    return False


def generate_decision_flop(analisys):
    ret = {}
    phase = 'FLOP'

    confidence_level = settings['STRATEGY'][phase][get_confidence_level(analisys, phase)]
    confidence_level_raise = settings['STRATEGY'][phase]['CONFIDENCE_DIFFERENCE_RAISE']
    hand_equity = analisys['hand_analisys']['RESULT'][0][1]
    is_hero_in_button = (analisys['hero']['POSITION'] == 'BUTTON')
    check_button_available = verify_check_command(analisys)

    logging.debug('generate_decision_flop({},{},{}), button:{} check:{}'.format(confidence_level, confidence_level_raise
                                                                                , hand_equity, is_hero_in_button,
                                                                                check_button_available))

    ret['RAISE_STRATEGY'] = settings['STRATEGY']['FLOP']['RAISE_STRATEGY']
    if hand_equity >= (confidence_level + confidence_level_raise):
        ret['DECISION'] = 'RAISE'
        return ret
    if hand_equity >= (confidence_level):
        ret['DECISION'] = 'CALL'
        return ret
    else:
        if is_hero_in_button and check_button_available and hand_equity > 0.5:
            logging.debug('BLUFFING!!! BLUFFING!!! BLUFFING!!! BLUFFING!!! BLUFFING!!!')
            ret['DECISION'] = 'RAISE'
        else:
            ret['DECISION'] = 'FOLD OR CHECK'

    return ret


def generate_decision(analisys):
    ret = {}
    try:
        phase = analisys['hand_analisys']['HAND_PHASE']
        if phase == 'PREFLOP':
            return generate_decision_preflop(analisys)
        else:
            return generate_decision_flop(analisys)
    except:
        ret['DECISION'] = 'FOLD OR CHECK'

    return ret


def has_command_to_execute(analisys):
    return not (
        analisys['commands']['COMMAND1'] == '' and analisys['commands']['COMMAND2'] == '' and analisys['commands'][
            'COMMAND3'] == '')


def generate_command(analisys):
    ret = {'TO_EXECUTE': 0}

    if not has_command_to_execute(analisys):
        return ret

    if analisys['decision']['DECISION'] == 'FOLD OR CHECK':
        for x in range(3):
            if 'CHECK' in analisys['commands']['COMMAND{}'.format(x + 1)].upper():
                ret['TO_EXECUTE'] = x + 1
                return ret
        for x in range(3):
            if 'FOLD' in analisys['commands']['COMMAND{}'.format(x + 1)].upper():
                ret['TO_EXECUTE'] = x + 1
                return ret

    if analisys['decision']['DECISION'] == 'RAISE':
        for x in range(3):
            if ('RAISE' in analisys['commands']['COMMAND{}'.format(x + 1)].upper() or
                        'BET' in analisys['commands']['COMMAND{}'.format(x + 1)].upper()):
                ret['TO_EXECUTE'] = x + 1
                return ret
        for x in range(3):
            if 'CALL' in analisys['commands']['COMMAND{}'.format(x + 1)].upper():
                ret['TO_EXECUTE'] = x + 1
                return ret
        for x in range(3):
            if 'CHECK' in analisys['commands']['COMMAND{}'.format(x + 1)].upper():
                ret['TO_EXECUTE'] = x + 1
                return ret

    if analisys['decision']['DECISION'] == 'CALL':
        for x in range(3):
            if 'CALL' in analisys['commands']['COMMAND{}'.format(x + 1)].upper():
                ret['TO_EXECUTE'] = x + 1
                return ret
        for x in range(3):
            if 'CHECK' in analisys['commands']['COMMAND{}'.format(x + 1)].upper():
                ret['TO_EXECUTE'] = x + 1
                return ret

    return ret


def generate_analisys(im):
    result = {'seats': 6, 'cards': analyse_players_with_cards(im), 'nocards': analyse_players_without_cards(im)}
    result['button'] = analyse_button(im)
    result['hero'] = analyse_hero(im, result['cards'], result['nocards'], result['button'])
    result['flop'] = analyse_flop_template(im)
    result['commands'] = analyse_commands(im)
    if has_command_to_execute(result):
        result['hand_analisys'] = analyse_hand(result)
        result['decision'] = generate_decision(result)
        result['command'] = generate_command(result)
    return result


def execute(args):
    if len(args) < 1:
        print("For this task you need at least 1 arguments: <Image Source> ")
        return
    image_name = args[0]
    im = grab_image_from_file(image_name)
    result = generate_analisys(im)
    pprint.PrettyPrinter().pprint(result)
