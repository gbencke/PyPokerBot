import logging
from settings import settings
from model.PokerStrategy import PokerStrategy
from model.PokerTableScanner import has_command_to_execute


class PokerStrategySimple(PokerStrategy):
    def __init__(self):
        PokerStrategy.__init__(self)

    def generate_command(self, analisys):
        ret = {'to_execute': 0}

        if not has_command_to_execute(analisys):
            return ret
        number_of_commands = len(analisys['commands'])

        if analisys['decision']['decision'] == 'FOLD OR CHECK':
            for x in range(number_of_commands):
                if 'CHECK' == analisys['commands'][x][0]:
                    ret['to_execute'] = x + 1
                    return ret
            for x in range(number_of_commands):
                if 'FOLD' == analisys['commands'][x][0]:
                    ret['to_execute'] = x + 1
                    return ret

        if analisys['decision']['decision'] == 'RAISE':
            for x in range(number_of_commands):
                if 'RAISE' == analisys['commands'][x][0] or 'BET' == analisys['commands'][x][0]:
                    ret['to_execute'] = x + 1
                    return ret
            for x in range(number_of_commands):
                if 'CALL' == analisys['commands'][x][0]:
                    ret['to_execute'] = x + 1
                    return ret
            for x in range(number_of_commands):
                if 'CHECK' == analisys['commands'][x][0]:
                    ret['to_execute'] = x + 1
                    return ret

        if analisys['decision']['decision'] == 'CALL':
            for x in range(number_of_commands):
                if 'CALL' in analisys['commands'][x][0]:
                    ret['to_execute'] = x + 1
                    return ret
            for x in range(number_of_commands):
                if 'CHECK' in analisys['commands'][x][0]:
                    ret['to_execute'] = x + 1
                    return ret

        return ret

    def get_current_call_value(self, analisys):
        call_button = [x for x in analisys['commands'] if x[0] == 'CALL']
        if len(call_button) > 0:
            return call_button[0][1]
        else:
            return 0

    def is_check_button_available(self, analisys):
        return len([x for x in analisys['commands'] if x[0] == 'CHECK']) > 0

    def position_button(self, analisys):
        return analisys['hero']['position'] == 'BUTTON' or analisys['hero']['position'] == 'LP'

    def position_out_position(self, analisys):
        return not ((analisys['hero']['position'] == 'BUTTON') or (analisys['hero']['position'] == 'LP'))

    def position_bb_check(self, analisys):
        return analisys['hero']['position'] == 'BB' and self.is_check_button_available(analisys)

    def position_button_check(self, analisys):
        return self.position_button(analisys) and self.is_check_button_available(analisys)

    def generate_pre_decision(self, analisys):
        try:
            phase = analisys['hand_analisys']['hand_phase']
            hand_equity = analisys['hand_analisys']['result'][0][1]

            if phase == 'PREFLOP':
                if self.position_button(analisys):
                    if hand_equity > 0.77:
                        return ('RAISE OR CALL', 20)
                    if hand_equity > 0.72:
                        return ('RAISE OR CALL', 10)
                    if hand_equity > 0.60:
                        return ('RAISE OR CALL', 5)
                if self.position_out_position(analisys):
                    if hand_equity > 0.77:
                        return ('RAISE OR CALL', 20)
                    if hand_equity > 0.72:
                        return ('RAISE OR CALL', 5)
                if self.position_bb_check(analisys):
                    if hand_equity > 0.77:
                        return ('RAISE OR CALL', 20)
                    if hand_equity > 0.72:
                        return ('RAISE OR CALL', 20)
                    if hand_equity > 0.60:
                        return ('RAISE OR CALL', 5)
            if phase == 'FLOP3':
                if self.position_button(analisys):
                    if hand_equity > 0.77:
                        return ('RAISE OR CALL', 20)
                    if hand_equity > 0.72:
                        return ('RAISE OR CALL', 10)
                    if hand_equity > 0.60:
                        return ('CALL OR FOLD', 5)
                if self.position_button_check(analisys):
                    if hand_equity > 0.77:
                        return ('RAISE OR CALL', 20)
                    if hand_equity > 0.72:
                        return ('RAISE OR CALL', 10)
                    if hand_equity > 0.60:
                        return ('RAISE OR CALL', 5)
                    return ('RAISE OR CALL', 5)
                if self.position_out_position(analisys):
                    if hand_equity > 0.77:
                        return ('RAISE OR CALL', 20)
                    if hand_equity > 0.72:
                        return ('RAISE OR CALL', 10)
                    if hand_equity > 0.60:
                        return ('CALL OR FOLD', 5)
            if phase == 'FLOP4':
                if self.position_button(analisys):
                    if hand_equity > 0.77:
                        return ('RAISE OR CALL', 40)
                    if hand_equity > 0.72:
                        return ('RAISE OR CALL', 20)
                    if hand_equity > 0.60:
                        return ('CALL OR FOLD', 10)
                if self.position_button_check(analisys):
                    if hand_equity > 0.77:
                        return ('RAISE OR CALL', 40)
                    if hand_equity > 0.72:
                        return ('RAISE OR CALL', 20)
                    if hand_equity > 0.60:
                        return ('RAISE OR CALL', 10)
                    return ('RAISE OR CALL', 10)
                if self.position_out_position(analisys):
                    if hand_equity > 0.77:
                        return ('RAISE OR CALL', 40)
                    if hand_equity > 0.72:
                        return ('RAISE OR CALL', 20)
                    if hand_equity > 0.60:
                        return ('CALL OR FOLD', 10)
            if phase == 'FLOP5':
                if self.position_button(analisys):
                    if hand_equity > 0.77:
                        return ('RAISE OR CALL', 40)
                    if hand_equity > 0.72:
                        return ('RAISE OR CALL', 20)
                    if hand_equity > 0.60:
                        return ('CALL OR FOLD', 10)
                if self.position_button_check(analisys):
                    if hand_equity > 0.77:
                        return ('RAISE OR CALL', 40)
                    if hand_equity > 0.72:
                        return ('RAISE OR CALL', 20)
                    if hand_equity > 0.60:
                        return ('RAISE OR CALL', 10)
                    return ('RAISE OR CALL', 10)
                if self.position_out_position(analisys):
                    if hand_equity > 0.77:
                        return ('RAISE OR CALL', 40)
                    if hand_equity > 0.72:
                        return ('RAISE OR CALL', 20)
                    if hand_equity > 0.60:
                        return ('CALL OR FOLD', 10)
        except:
            pass
        return ('FOLD OR CHECK', 0)

    def generate_decision(self, analisys):
        decision = self.generate_pre_decision(analisys)
        current_call_value = self.get_current_call_value(analisys)
        if current_call_value == '':
            current_call_value = 0
        if decision[0] == 'RAISE OR CALL':
            if current_call_value > decision[1]:
                return {'decision': 'CALL', 'raise_strategy': '0'}
            else:
                return {'decision': 'RAISE', 'raise_strategy': decision[1]}
        if decision[0] == 'CALL OR FOLD':
            if current_call_value > decision[1]:
                return {'decision': 'FOLD', 'raise_strategy': '0'}
            else:
                return {'decision': 'CALL', 'raise_strategy': '0'}
        return {'decision': 'FOLD OR CHECK', 'raise_strategy': '0'}

    def run_strategy(self, result):
        if has_command_to_execute(result):
            result['decision'] = self.generate_decision(result)
            result['command'] = self.generate_command(result)
        return result
