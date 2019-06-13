from PIL import Image

def grab_image_from_file(image):
    """
    Loads a certain image from a filename and returns a numpy array representing it.

    :param image: The filename to load.
    :return: The numpy array representing the image
    """
    return Image.open(image)


def grab_image_pos_from_image(image, pos, size):
    """
    Returns a region of the image based on a certain position and size.

    :param image: The numpy array representing the image
    :param pos: The Top-Left position
    :param size: The size of the image
    :return: A numpy array of the region, representing the image.
    """
    return image.crop((pos[0], pos[1], pos[0] + size[0], pos[1] + size[1]))


def grab_image_pos_from_file(file_name, pos, size):
    """
    Returns a region of the image in the file name specified, based on a certain position and size

    :param file_name: The file name of the image
    :param pos: The Top-Left position
    :param size: The size of the image
    :return: A numpy array of the region, representing the image.
    """
    image_to_analyse = Image.open(file_name)
    return grab_image_pos_from_image(image_to_analyse, pos, size)
