class PokerStrategy:
    def __init__(self):
        pass

    def has_command_to_execute(self, analisys):
        return not (
            analisys['commands'][0] == '' and analisys['commands'][1] == '' and analisys['commands'][2] == '')


    def verify_check_command(self, analisys):
        for x in range(3):
            if 'CHECK' in analisys['commands'][x].upper():
                return True
        return False
