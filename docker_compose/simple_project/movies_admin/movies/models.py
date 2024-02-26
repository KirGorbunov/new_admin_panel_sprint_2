import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedCreatedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class TimeStampedModifiedMixin(models.Model):
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedCreatedMixin, TimeStampedModifiedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        db_table = "content\".\"genre"
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedCreatedMixin, TimeStampedModifiedMixin):
    full_name = models.CharField(_('name'), max_length=255)

    class Meta:
        db_table = "content\".\"person"
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        return self.full_name


class Filmwork(UUIDMixin, TimeStampedCreatedMixin, TimeStampedModifiedMixin):
    class Type(models.TextChoices):
        movie = "movie", _("Movie")
        tv_show = "tv_show", _("TV show")

    title = models.CharField(_('title'), max_length=255)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'), blank=True, null=True)
    file_path = models.FileField(_('file'), blank=True, null=True, upload_to='movies/')
    rating = models.FloatField(_('rating'), blank=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    type = models.CharField(_('type'), max_length=7, choices=Type.choices, default=Type.movie)
    genres = models.ManyToManyField(Genre, verbose_name=_('genres'), through='GenreFilmwork')

    class Meta:
        db_table = "content\".\"film_work"
        verbose_name = _('Film work')
        verbose_name_plural = _('Film works')

        def __str__(self):
            return self.title


class GenreFilmwork(UUIDMixin, TimeStampedCreatedMixin):
    film_work = models.ForeignKey('Filmwork', verbose_name=_('film work'), on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', verbose_name=_('genre'), on_delete=models.CASCADE)

    class Meta:
        db_table = "content\".\"genre_film_work"
        verbose_name = _('Genre of film work')
        verbose_name_plural = _('Genres of film works')
        constraints = [
            models.UniqueConstraint(fields=['film_work_id', 'genre_id'], name='film_work_genre_idx')
        ]


class PersonFilmwork(UUIDMixin, TimeStampedCreatedMixin):
    film_work = models.ForeignKey('Filmwork', verbose_name=_('film work'), on_delete=models.CASCADE)
    person = models.ForeignKey('Person', verbose_name=_('person'), on_delete=models.CASCADE)
    role = models.TextField(_('role'))

    class Meta:
        db_table = "content\".\"person_film_work"
        verbose_name = _('Person of film work')
        verbose_name_plural = _('Persons of film works')
        constraints = [
            models.UniqueConstraint(fields=['film_work_id', 'person_id', 'role'], name='film_work_person_role_idx')
        ]
