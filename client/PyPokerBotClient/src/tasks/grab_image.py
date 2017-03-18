from settings import settings
from helpers.win32.screenshot import grab_image_pos_from_file


def execute(args):
    if len(args) < 4:
        print("For this task you need at least 3 arguments: <Image Source> <Pos> <size> <FileName to save>")
        return
    image_source = args[0]
    image_pos = args[1]
    image_size = args[2]
    image_filename_to_save = args[3]
    im = grab_image_pos_from_file(image_source, settings['TABLE_SCANNER'][image_pos], settings['TABLE_SCANNER'][image_size])
    im.save(image_filename_to_save)
