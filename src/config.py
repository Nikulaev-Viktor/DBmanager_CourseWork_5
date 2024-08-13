from configparser import ConfigParser


def config(filename='database.ini', section='postgresql'):
    """Функция для чтения содержимого файла конфигурации database.ini
     итерирует по парам ключ-значение этой секции и добавляет их в словарь db"""
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[params[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db




