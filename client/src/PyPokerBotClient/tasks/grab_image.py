"""
This task is used to debug the computer vision process that identifies the objects on the
screenshot taken from the poker table. It crops the image in a specific position and size

Usage:
::

    python PyPokerBot.py grab_image <Image Source> <Platform> <TableType> <Pos> <size> <FileName>


Parameters:

    **Image Source**: The Screenshot of the poker client to be used as source

    **Platform**: The poker platform from which the screenshot was taken

    **TableType**: The type of table that the screenshot was taken (6-SEAT,9-SEAT,etc...)

    **Pos**: The position to be cropped

    **Size**: The size of the image to be cropped

    **Filename to Save**: The filename for the cropped image

Return:

    **None** (But saves the image as specifiec in the parameter above)

Obs:

    It is important to notice that the position and size specified are
    defined on the settings.py file.

"""
from PyPokerBotClient.settings import GLOBAL_SETTINGS as Settings
from PyPokerBotClient.osinterface.win32.screenshot import grab_image_pos_from_file


def usage():
    """Display the current task (grab image) usage

    :return:  None (Prints the usage information to stdout)
    """
    return \
"""
This task is used to debug the computer vision process that identifies the objects on the
screenshot taken from the poker table. It crops the image in a specific position and size

Usage:
::

    python PyPokerBot.py grab_image <Image Source> <Platform> <TableType> <Pos> <size> <FileName>


Parameters:

    **Image Source**: The Screenshot of the poker client to be used as source

    **Platform**: The poker platform from which the screenshot was taken

    **TableType**: The type of table that the screenshot was taken (6-SEAT,9-SEAT,etc...)

    **Pos**: The position to be cropped

    **Size**: The size of the image to be cropped

    **Filename to Save**: The filename for the cropped image

Return:

    **None** (But saves the image as specifiec in the parameter above)

Obs:

    It is important to notice that the position and size specified are
    defined on the settings.py file.

"""


def execute(args):
    """
    This task is used to debug the computer vision process that identifies the objects on the
    screenshot taken from the poker table. It crops the image in a specific position and size

    :param args: The Command Line parameters specified on the module description above which are:
         <Image Source> <Platform> <TableType> <Pos> <size> <FileName to save>

    :return: None (But saves the image as specifiec in the parameter above)


    """
    if len(args) < 4:
        print(
            "For this task you need at least 3 arguments: " +
            " <Image Source> <Platform> <TableType> <Pos> <size> <FileName to save>")
        return
    image_source = args[0]
    image_platform = args[1]
    image_tabletype = args[2]
    image_pos = args[3]
    image_size = args[4]
    image_filename_to_save = args[5]
    table_image_grabbed = grab_image_pos_from_file(
        image_source,
        Settings.get_raw_image_pos(image_platform, image_tabletype, image_pos),
        Settings.get_raw_image_size(image_platform, image_tabletype, image_size))
    table_image_grabbed.save(image_filename_to_save)
