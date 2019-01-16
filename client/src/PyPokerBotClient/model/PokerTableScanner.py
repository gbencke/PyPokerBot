import logging


def has_command_to_execute(analisys):
    return not (
        analisys['commands'][0][0] == '' and analisys['commands'][1][0] == '' and analisys['commands'][2][0] == '')


class PokerTableScanner(object):
    suits = ['h', 's', 'c', 'd']
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

    def __init__(self, TableType, NumberOfSeats, BB, SB):
        self.TableType = TableType
        self.NumberOfSeats = NumberOfSeats
        self.BB = BB
        self.SB = SB


    def get_offset_for_numbers(self, selected_image, right_to_left):
        pixel_height_to_test = range(3)

        if right_to_left:
            start = selected_image.width - 1
            stop = 10
            step = -1
        else:
            start = 10
            stop = selected_image.width - 1
            step = 1

        continued_green = 0
        offset = 0
        for w in range(start, stop, step):
            red = 0
            blue = 0
            green = 0
            black = 0
            white = 0

            for h in pixel_height_to_test:
                pixel = selected_image.getpixel((w, h))
                if pixel[0] >= 230 and pixel[1] >= 230 and pixel[2] >= 230:
                    white += 1
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
            if green == len(pixel_height_to_test):
                continued_green += 1
            else:
                continued_green = 0
            offset += 1
            if continued_green >= 4:
                return offset-3, selected_image.width - 1, 1
        return 0

    @staticmethod
    def generate_analisys_summary_debug(message):
        for x in message.split('\n'):
            logging.debug(x)

    @staticmethod
    def generate_analisys_summary_info(message):
        for x in message.split('\n'):
            logging.info(x)


