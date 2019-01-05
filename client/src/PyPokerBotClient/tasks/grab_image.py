from PyPokerBotClient.settings import GlobalSettings as Settings
from PyPokerBotClient.osinterface.win32.screenshot import grab_image_pos_from_file


def usage():
    return "Test"


def execute(args):
    if len(args) < 4:
        print(
            "For this task you need at least 3 arguments: <Image Source> <Platform> <TableType> <Pos> <size> <FileName to save>")
        return
    image_source = args[0]
    image_platform = args[1]
    image_tabletype = args[2]
    image_pos = args[3]
    image_size = args[4]
    image_filename_to_save = args[5]
    im = grab_image_pos_from_file(
        image_source,
        Settings.get_raw_image_pos(image_platform, image_tabletype, image_pos),
        Settings.get_raw_image_size(image_platform, image_tabletype, image_pos))
    im.save(image_filename_to_save)
