def get_table_name(title):
    return title.split('-')[0].strip()


def get_table_stakes(title):
    return title.split('-')[1].strip()


def get_table_format(title):
    return title.split('-')[2].strip()
