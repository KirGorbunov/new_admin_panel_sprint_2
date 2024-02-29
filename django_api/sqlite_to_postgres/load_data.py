import errno
import logging.config
import os.path
import sqlite3
import sys
from contextlib import closing
from dataclasses import astuple, dataclass

import psycopg2
from dataclasses_storage import (FilmWork, Genre, GenreFilmWork, Person,
                                 PersonFilmWork)
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor, execute_values

logging.config.fileConfig(os.path.dirname(os.path.realpath(__file__))+"/logger.conf")


class PostgresSaver:
    def __init__(self, pg_conn: _connection):
        self.connect = pg_conn

    def get_postgres_fields_name(self):
        """Получение имен полей Postgres"""
        cursor = self.connect.cursor()
        try:
            cursor.execute(f"SELECT * FROM {db_dataclass.table_name} LIMIT 0")
            column_names = [desc[0] for desc in cursor.description]
            self.column_names_str = ",".join(column_names)
        except Exception:
            logging.exception(f"Error retrieving column names from {db_dataclass.table_name} table Postgres database")
            sys.exit(1)
        else:
            logging.info(f"Retrieved column names from {db_dataclass.table_name} table Postgres database")

    def save_all_data(self, data: list):
        """Загрузка данных в Postgres"""
        cursor = self.connect.cursor()
        try:
            data = [astuple(movie) for movie in data]
            query = (
                f"INSERT INTO {db_dataclass.table_name} ({self.column_names_str}) VALUES %s"
                f"ON CONFLICT (id) DO NOTHING"
            )
            execute_values(cursor, query, data)
            self.connect.commit()
        except Exception:
            logging.exception(f"Error inserting data to {db_dataclass.table_name} table Postgres database")
            sys.exit(1)
        else:
            logging.info(f"Inserted {n} rows to {db_dataclass.table_name} table Postgres database")


class SQLiteExtractor:
    def __init__(self, connection: sqlite3.Connection):
        self.connect = connection

    def extract_movies(self, db_dataclass: dataclass, n: int):
        """Метод выгрузки данных из SQLite"""
        self.connect.row_factory = sqlite3.Row
        cursor = self.connect.cursor()
        try:
            cursor.execute(f"SELECT * FROM {db_dataclass.table_name};")
            while True:
                rows = cursor.fetchmany(n)
                if not rows:
                    break
                yield [[(db_dataclass(**i)) for i in rows]]
        except Exception:
            logging.exception(f"Error retrieving data from {db_dataclass.table_name} table SQLite database")
            sys.exit(1)
        else:
            logging.info(f"Retrieved all rows from {db_dataclass.table_name} table SQLite database")


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection, bd_dataclass: dataclass, n: int):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)
    postgres_saver.get_postgres_fields_name()

    for data in sqlite_extractor.extract_movies(bd_dataclass, n):
        postgres_saver.save_all_data(*data)


if __name__ == "__main__":
    n = 10
    file_sqlite_db_path = os.path.dirname(os.path.realpath(__file__))+"/db.sqlite"
    dsl = {
        "dbname": os.environ.get("POSTGRES_DB"),
        "user": os.environ.get("POSTGRES_USER"),
        "password": os.environ.get("POSTGRES_PASSWORD"),
        "host": os.environ.get("DB_HOST", "127.0.0.1"),
        "port": os.environ.get("DB_PORT", 5432),
        "options": "-c search_path=content"
    }

    try:
        if os.path.exists(file_sqlite_db_path):
            with closing(sqlite3.connect(file_sqlite_db_path)) as sqlite_conn, \
                    closing(psycopg2.connect(**dsl, cursor_factory=DictCursor)) as pg_conn:
                for db_dataclass in [FilmWork, Genre, Person, GenreFilmWork, PersonFilmWork]:
                    load_from_sqlite(sqlite_conn, pg_conn, db_dataclass, n)
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_sqlite_db_path)
    except FileNotFoundError:
        logging.exception("Not such file of SQLite database: file_sqlite_db_path")
    except sqlite3.Error:
        logging.exception("Problems to connect to SQLite database")
    except psycopg2.Error:
        logging.exception("Problems to connect to Postgres database")
