class PokerStrategy:
    def __init__(self):
        pass

    def has_command_to_execute(self, analisys):
        return not (
            analisys['commands']['COMMAND1'] == '' and analisys['commands']['COMMAND2'] == '' and analisys['commands'][
                'COMMAND3'] == '')

    def verify_check_command(self, analisys):
        for x in range(3):
            if 'CHECK' in analisys['commands']['COMMAND{}'.format(x + 1)].upper():
                return True
        return False
