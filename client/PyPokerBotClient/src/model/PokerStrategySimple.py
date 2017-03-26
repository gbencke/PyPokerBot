import ast
import logging
import os
import numpy
import cv2
import datetime
import subprocess
import requests

from time import sleep
from datetime import datetime
from settings import settings
from platforms.utils import get_histogram_from_image
from osinterface.win32.screenshot import grab_image_from_file, grab_image_pos_from_image
from model.PokerStrategy import PokerStrategy


class PokerStrategySimple(PokerStrategy):
    def __init__(self):
        PokerStrategy.__init__(self)

    def get_confidence_level(self, analisys, phase):
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

    def generate_decision_preflop(self, analisys):
        ret = {}
        phase = 'PREFLOP'

        confidence_level = settings['STRATEGY'][phase][self.get_confidence_level(analisys, phase)]
        confidence_level_raise = settings['STRATEGY'][phase]['CONFIDENCE_DIFFERENCE_RAISE']
        hand_equity = analisys['hand_analisys']['RESULT'][0][1]
        is_hero_in_button = (analisys['hero']['POSITION'] == 'BUTTON')

        logging.debug(
            'generate_decision_preflop({},{},{}) button:{}'.format(confidence_level, confidence_level_raise,
                                                                   hand_equity,
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

    def verify_check_command(self, analisys):
        for x in range(3):
            if 'CHECK' in analisys['commands']['COMMAND{}'.format(x + 1)].upper():
                return True
        return False

    def generate_decision_flop(self, analisys):
        ret = {}
        phase = 'FLOP'

        confidence_level = settings['STRATEGY'][phase][self.get_confidence_level(analisys, phase)]
        confidence_level_raise = settings['STRATEGY'][phase]['CONFIDENCE_DIFFERENCE_RAISE']
        hand_equity = analisys['hand_analisys']['RESULT'][0][1]
        is_hero_in_button = (analisys['hero']['POSITION'] == 'BUTTON')
        check_button_available = self.verify_check_command(analisys)

        logging.debug(
            'generate_decision_flop({},{},{}), button:{} check:{}'.format(confidence_level, confidence_level_raise
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

    def generate_decision(self, analisys):
        ret = {}
        try:
            phase = analisys['hand_analisys']['HAND_PHASE']
            if phase == 'PREFLOP':
                return self.generate_decision_preflop(analisys)
            else:
                return self.generate_decision_flop(analisys)
        except:
            ret['DECISION'] = 'FOLD OR CHECK'

        return ret

    def has_command_to_execute(self, analisys):
        return not (
            analisys['commands']['COMMAND1'] == '' and analisys['commands']['COMMAND2'] == '' and analisys['commands'][
                'COMMAND3'] == '')

    def generate_command(self, analisys):
        ret = {'TO_EXECUTE': 0}

        if not self.has_command_to_execute(analisys):
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

    def analyse_commands(self, im):
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
                return_from_tesseract = subprocess.check_output(['tesseract', command_image_name, 'stdout'],
                                                                shell=False)
                if len(return_from_tesseract.strip()) == 0:
                    error_filename = command_image_name + '.error.' + datetime.now().strftime(
                        "%Y%m%d%H%M%S.%f") + '.jpg'
                    logging.debug("ERROR ON TESSERACT!!! " + error_filename)
                    im_command.save(error_filename)
                ret['COMMAND{}'.format(current_command)] = return_from_tesseract.replace('\r\n', ' ').replace('  ', ' ')
                os.remove(command_image_name)
                sleep(0.2)
        return ret

    def analyse_hand(self, analisys):
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

    def run_strategy(self, result):
        if self.has_command_to_execute(result):
            result['hand_analisys'] = self.analyse_hand(result)
            result['decision'] = self.generate_decision(result)
            result['command'] = self.generate_command(result)
        return result
