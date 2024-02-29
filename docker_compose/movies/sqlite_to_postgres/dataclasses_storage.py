import datetime
import uuid
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class FilmWork:
    id: uuid.UUID
    title: str
    description: str
    creation_date: datetime.date
    rating: float
    type: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    file_path: str
    table_name: ClassVar[str] = "film_work"
    field_name_sqlite: ClassVar[list] = [
                                         "id",
                                         "title",
                                         "description",
                                         "creation_date",
                                         "file_path",
                                         "rating",
                                         "type",
                                         "created_at",
                                         "updated_at"
                                        ]
    field_name_postgres: ClassVar[list] = [
                                            "id",
                                            "title",
                                            "description",
                                            "creation_date",
                                            "file_path",
                                            "rating",
                                            "type",
                                            "created",
                                            "modified"
                                            ]


@dataclass
class Genre:
    table_name: ClassVar[str] = "genre"
    id: uuid.UUID
    name: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    field_name_sqlite: ClassVar[list] = [
                                         "id",
                                         "name",
                                         "description",
                                         "created_at",
                                         "updated_at"
                                        ]
    field_name_postgres: ClassVar[list] = [
                                            "id",
                                            "name",
                                            "description",
                                            "created",
                                            "modified"
                                            ]


@dataclass
class Person:
    table_name: ClassVar[str] = "person"
    id: uuid.UUID
    full_name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    field_name_sqlite: ClassVar[list] = [
                                         "id",
                                         "full_name",
                                         "created_at",
                                         "updated_at"
                                        ]
    field_name_postgres: ClassVar[list] = [
                                            "id",
                                            "full_name",
                                            "created",
                                            "modified"
                                            ]


@dataclass
class GenreFilmWork:
    table_name: ClassVar[str] = "genre_film_work"
    id: uuid.UUID
    genre_id: uuid.UUID
    film_work_id: uuid.UUID
    created_at: datetime.datetime
    field_name_sqlite: ClassVar[list] = [
                                        "id",
                                        "genre_id",
                                        "film_work_id",
                                        "created_at",
                                        ]
    field_name_postgres: ClassVar[list] = [
                                        "id",
                                        "genre_id",
                                        "film_work_id",
                                        "created",
                                        ]


@dataclass
class PersonFilmWork:
    table_name: ClassVar[str] = "person_film_work"
    id: uuid.UUID
    person_id: uuid.UUID
    film_work_id: uuid.UUID
    role: str
    created_at: datetime.datetime
    field_name_sqlite: ClassVar[list] = [
                                        "id",
                                        "person_id",
                                        "film_work_id",
                                        "role",
                                        "created_at",
                                        ]
    field_name_postgres: ClassVar[list] = [
                                        "id",
                                        "person_id",
                                        "film_work_id",
                                        "role",
                                        "created",
                                        ]
