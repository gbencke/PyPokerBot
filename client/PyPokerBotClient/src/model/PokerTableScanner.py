class PokerTableScanner:
    suits = ['h', 's', 'c', 'd']
    cards = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

    def __init__(self, TableType, NumberOfSeats, BB, SB):
        self.TableType = TableType
        self.NumberOfSeats = NumberOfSeats
        self.BB = BB
        self.SB = SB

    def get_suite_from_image(self, selected_image):
        red = 0
        blue = 0
        green = 0
        black = 0
        for w in range(selected_image.width):
            for h in range(selected_image.height):
                pixel = selected_image.getpixel((w, h))
                if pixel[0] >= 230 and pixel[1] >= 230 and pixel[2] >= 230:
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
        if black > 200:
            return 's'
        if red > green and red > blue and red > black:
            return 'h'
        if green > red and green > blue and green > black:
            return 'c'
        if blue > red and blue > green and blue > black:
            return 'd'
