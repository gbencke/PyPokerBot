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
            if analisys['cards'][x] == 'CARD':
                total_villains += 1
        if total_villains == 1:
            return 'CONFIDENCE_LEVEL_HEADS_UP'
        else:
            if analisys['hero']['position'] == 'BUTTON':
                return 'CONFIDENCE_LEVEL_POSITION'
            else:
                return 'CONFIDENCE_LEVEL'

    def generate_decision_preflop(self, analisys):
        ret = {}
        phase = 'PREFLOP'

        confidence_level = settings['STRATEGIES']['SIMPLE'][phase][self.get_confidence_level(analisys, phase)]
        confidence_level_raise = settings['STRATEGIES']['SIMPLE'][phase]['CONFIDENCE_DIFFERENCE_RAISE']
        hand_equity = analisys['hand_analisys']['result'][0][1]
        ret['raise_strategy'] = settings['STRATEGY']['FLOP']['RAISE_STRATEGY']
        if hand_equity >= (confidence_level + confidence_level_raise):
            ret['decision'] = 'RAISE'
            return ret
        if hand_equity >= confidence_level:
            ret['decision'] = 'CALL'
            return ret
        else:
            ret['decision'] = 'FOLD OR CHECK'
        return ret

    def generate_decision_flop(self, analisys):
        ret = {}
        phase = 'FLOP'

        confidence_level =  settings['STRATEGIES']['SIMPLE'][phase][self.get_confidence_level(analisys, phase)]
        confidence_level_raise =  settings['STRATEGIES']['SIMPLE'][phase]['CONFIDENCE_DIFFERENCE_RAISE']
        hand_equity = analisys['hand_analisys']['result'][0][1]
        is_hero_in_button = (analisys['hero']['position'] == 'BUTTON')
        check_button_available = self.verify_check_command(analisys)

        ret['RAISE_STRATEGY'] = settings['STRATEGIES']['SIMPLE'][phase]['RAISE_STRATEGY']
        if hand_equity >= (confidence_level + confidence_level_raise):
            ret['decision'] = 'RAISE'
            return ret
        if hand_equity >= confidence_level:
            ret['decision'] = 'CALL'
            return ret
        else:
            if is_hero_in_button and check_button_available and hand_equity > 0.5:
                logging.debug('BLUFFING!!! BLUFFING!!! BLUFFING!!! BLUFFING!!! BLUFFING!!!')
                ret['decision'] = 'RAISE'
            else:
                ret['decision'] = 'FOLD OR CHECK'

        return ret

    def generate_decision(self, analisys):
        ret = {}
        try:
            phase = analisys['hand_analisys']['hand_phase']
            if phase == 'PREFLOP':
                return self.generate_decision_preflop(analisys)
            else:
                return self.generate_decision_flop(analisys)
        except:
            ret['decision'] = 'FOLD OR CHECK'

        return ret

    def generate_command(self, analisys):
        ret = {'to_execute': 0}

        if not self.has_command_to_execute(analisys):
            return ret

        if analisys['decision']['decision'] == 'FOLD OR CHECK':
            for x in range(3):
                if 'CHECK' in analisys['commands'][x].upper():
                    ret['to_execute'] = x + 1
                    return ret
            for x in range(3):
                if 'FOLD' in analisys['commands'][x].upper():
                    ret['to_execute'] = x + 1
                    return ret

        if analisys['decision']['decision'] == 'RAISE':
            for x in range(3):
                if ('RAISE' in analisys['commands'][x].upper() or
                            'BET' in analisys['commands'][x].upper()):
                    ret['to_execute'] = x + 1
                    return ret
            for x in range(3):
                if 'CALL' in analisys['commands'][x].upper():
                    ret['to_execute'] = x + 1
                    return ret
            for x in range(3):
                if 'CHECK' in analisys['commands'][x].upper():
                    ret['to_execute'] = x + 1
                    return ret

        if analisys['decision']['decision'] == 'CALL':
            for x in range(3):
                if 'CALL' in analisys['commands'][x].upper():
                    ret['to_execute'] = x + 1
                    return ret
            for x in range(3):
                if 'CHECK' in analisys['commands'][x].upper():
                    ret['to_execute'] = x + 1
                    return ret

        return ret

    def run_strategy(self, result):
        if self.has_command_to_execute(result):
            result['decision'] = self.generate_decision(result)
            result['command'] = self.generate_command(result)
        return result
