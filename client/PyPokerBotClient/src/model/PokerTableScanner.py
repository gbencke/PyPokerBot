

class PokerTableScanner:
    def __init__(self, TableType, NumberOfSeats, BB, SB):
        self.TableType = TableType
        self.NumberOfSeats = NumberOfSeats
        self.BB = BB
        self.SB = SB


    suits = ['h', 's', 'c', 'd']
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

