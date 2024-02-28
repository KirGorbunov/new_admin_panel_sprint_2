import datetime
import os.path
import sqlite3

import psycopg2
from dataclasses_storage import (FilmWork, Genre, GenreFilmWork, Person,
                                 PersonFilmWork)
from psycopg2.extras import DictCursor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
file_sqlite_db_path = os.path.join(BASE_DIR, "db.sqlite")
dsl = {
    'dbname': 'movies_database',
    'user': 'app', 'password': '123qwe',
    'host': 'localhost', 'port': 5432,
    'options': '-c search_path=content'
}


def convert_timestamp(val):
    """Convert Unix epoch timestamp to datetime.datetime object."""
    return datetime.datetime.fromisoformat(val.decode())


sqlite3.register_converter("timestamp", convert_timestamp)


def test_database_count():
    assert get_count_sqllite(file_sqlite_db_path) == get_count_postgres(dsl)


def test_database_all_data():
    assert get_all_sqllite(file_sqlite_db_path) == get_all_postgres(dsl)


def get_count_sqllite(file_sqlite_db_path: str):
    sqlite_db_counter = []
    with sqlite3.connect(file_sqlite_db_path) as sqlite_conn:
        for bd_dataclass in [FilmWork, Genre, Person, GenreFilmWork, PersonFilmWork]:
            cursor = sqlite_conn.cursor()
            print(bd_dataclass.table_name)
            query = f"SELECT COUNT(*) FROM {bd_dataclass.table_name};"
            print(query)
            cursor.execute(query)
            sqlite_table_counter = cursor.fetchall()
            sqlite_db_counter.append(list(*sqlite_table_counter))
    return sqlite_db_counter


def get_count_postgres(dsl):
    postgres_db_counter = []
    with psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        for bd_dataclass in [FilmWork, Genre, Person, GenreFilmWork, PersonFilmWork]:
            cursor = pg_conn.cursor()
            query = f"SELECT COUNT(*) FROM {bd_dataclass.table_name};"
            cursor.execute(query)
            postgres_table_counter = cursor.fetchall()
            postgres_db_counter.append(*postgres_table_counter)
    return postgres_db_counter


def get_all_sqllite(file_sqlite_db_path: str):
    sqlite_all = []
    with sqlite3.connect(file_sqlite_db_path, detect_types=sqlite3.PARSE_DECLTYPES) as sqlite_conn:
        sqlite_conn.row_factory = lambda cursor, row: list(row)
        for bd_dataclass in [FilmWork, Genre, Person, GenreFilmWork, PersonFilmWork]:
            cursor = sqlite_conn.cursor()
            fields = ','.join(bd_dataclass.field_name_sqlite)
            query = f"SELECT {fields} FROM {bd_dataclass.table_name};"
            cursor.execute(query)
            sqlite_table_all = cursor.fetchall()
            sqlite_all.append(sqlite_table_all)
    return sqlite_all


def get_all_postgres(dsl):
    postgres_all = []
    with psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        for bd_dataclass in [FilmWork, Genre, Person, GenreFilmWork, PersonFilmWork]:
            cursor = pg_conn.cursor()
            fields = ','.join(bd_dataclass.field_name_postgres)
            query = f"SELECT {fields} FROM {bd_dataclass.table_name};"
            cursor.execute(query)
            postgres_table_all = cursor.fetchall()
            postgres_all.append(postgres_table_all)
    return postgres_all
