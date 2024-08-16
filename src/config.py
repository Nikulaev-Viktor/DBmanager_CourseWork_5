from configparser import ConfigParser
import os

ROOT_DIR = os.path.dirname(__file__)


def config(filename='D:/pythonProject/DBmanager_CourseWork_5/src/database.ini', section="postgresql"):

    """Функция для чтения содержимого файла конфигурации database.ini
         итерирует по парам ключ-значение этой секции и добавляет их в словарь db"""

    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db