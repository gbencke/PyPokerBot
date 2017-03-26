from settings import settings
from osinterface.win32.screenshot import grab_image_pos_from_file


def execute(args):
    if len(args) < 4:
        print("For this task you need at least 3 arguments: <Image Source> <Platform> <TableType> <Pos> <size> <FileName to save>")
        return
    image_source = args[0]
    image_platform = args[1]
    image_tabletype = args[2]
    image_pos = args[3]
    image_size = args[4]
    image_filename_to_save = args[5]
    im = grab_image_pos_from_file(
        image_source,
        settings[image_platform]['TABLE_SCANNER'][image_tabletype][image_pos],
        settings[image_platform]['TABLE_SCANNER'][image_tabletype][image_size])
    im.save(image_filename_to_save)
