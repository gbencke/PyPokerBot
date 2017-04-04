class PokerStrategy:
    def __init__(self):
        pass



    def verify_check_command(self, analisys):
        for x in range(3):
            if 'CHECK' in analisys['commands'][x].upper():
                return True
        return False
