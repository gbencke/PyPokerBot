


def is_pokerstars_lobby(classname, window_text):
    if 'POKERSTARS LOBBY' in window_text.upper():
        return True

def is_pokerstars_table(classname, window_text):
    if 'PokerStarsTableFrameClass'.upper() in classname.upper():
        return True




