import psycopg2

from configparser import ConfigParser

def config(filename="database.ini", section="postgresql"):
    """
    читаем данные из файла filename секции section

    пример файла
        > [postgresql]
        > host=localhost
        > user=postgres
        > password=12345
        > port=5432


    :param filename: имя файла, по умолчанию database.ini
    :param section: имя секции, по умолчанию postgresql
    :return: возвращает список прочитанных параметров или ошибку если секции
    нет в указанном файле
    """
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]

    # 2 вариант
    # if parser.has_section(section):
    #     params = parser.items(section)
    #     db = dict(params)

    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db

def create_database(database_name: str, params: dict):
    """
    Создание базы данных и таблиц
    database_name - имя базы данных
    params - список параметров для подключения
    """

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True

    with conn.cursor() as cur:
        # удаление базы если она есть
        cur.execute(f"DROP DATABASE IF EXISTS {database_name}")

        cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    # with conn.cursor() as cur:
    #     cur.execute("""
    #         CREATE TABLE channels (
    #             channel_id SERIAL PRIMARY KEY,
    #             title VARCHAR(255) NOT NULL,
    #             views INTEGER,
    #             subscribers INTEGER,
    #             videos INTEGER,
    #             channel_url TEXT
    #         )
    #     """)

    conn.commit()

    # with conn.cursor() as cur:
    #     cur.execute("""
    #         CREATE TABLE videos (
    #             video_id SERIAL PRIMARY KEY,
    #             channel_id INT REFERENCES channels(channel_id),
    #             title VARCHAR NOT NULL,
    #             publish_date DATE,
    #             video_url TEXT
    #         )
    #     """)

    conn.commit()
    conn.close()