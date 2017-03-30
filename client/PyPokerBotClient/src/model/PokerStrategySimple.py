import logging
from settings import settings
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

        confidence_level = settings['STRATEGIES']['SIMPLE'][phase][self.get_confidence_level(analisys, phase)]
        confidence_level_raise = settings['STRATEGIES']['SIMPLE'][phase]['CONFIDENCE_DIFFERENCE_RAISE']
        hand_equity = analisys['hand_analisys']['RESULT'][0][1]
        ret['RAISE_STRATEGY'] = settings['STRATEGY']['FLOP']['RAISE_STRATEGY']
        if hand_equity >= (confidence_level + confidence_level_raise):
            ret['DECISION'] = 'RAISE'
            return ret
        if hand_equity >= confidence_level:
            ret['DECISION'] = 'CALL'
            return ret
        else:
            ret['DECISION'] = 'FOLD OR CHECK'
        return ret

    def generate_decision_flop(self, analisys):
        ret = {}
        phase = 'FLOP'

        confidence_level =  settings['STRATEGIES']['SIMPLE'][phase][self.get_confidence_level(analisys, phase)]
        confidence_level_raise =  settings['STRATEGIES']['SIMPLE'][phase]['CONFIDENCE_DIFFERENCE_RAISE']
        hand_equity = analisys['hand_analisys']['RESULT'][0][1]
        is_hero_in_button = (analisys['hero']['POSITION'] == 'BUTTON')
        check_button_available = self.verify_check_command(analisys)

        ret['RAISE_STRATEGY'] = settings['STRATEGIES']['SIMPLE'][phase]['RAISE_STRATEGY']
        if hand_equity >= (confidence_level + confidence_level_raise):
            ret['DECISION'] = 'RAISE'
            return ret
        if hand_equity >= confidence_level:
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

    def run_strategy(self, result):
        if self.has_command_to_execute(result):
            result['decision'] = self.generate_decision(result)
            result['command'] = self.generate_command(result)
        return result
