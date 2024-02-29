from django.conf import settings
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movies.models import Filmwork


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ["get"]

    def get_queryset(self):
        return Filmwork.objects.prefetch_related("genres", "persons") \
            .values("id", "title", "description", "creation_date", "rating", "type") \
            .annotate(genres=ArrayAgg("genres__name", distinct=True),
                      actors=ArrayAgg("persons__full_name",
                                      distinct=True,
                                      filter=Q(personfilmwork__role="actor")),
                      directors=ArrayAgg("persons__full_name",
                                         distinct=True,
                                         filter=Q(personfilmwork__role="director")),
                      writers=ArrayAgg("persons__full_name",
                                       distinct=True,
                                       filter=Q(personfilmwork__role="writer")))

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = settings.PAGINATE_BY

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )

        if not page.has_previous():
            return {"count": paginator.count,
                    "total_pages": paginator.num_pages,
                    "prev": None,
                    "next": page.next_page_number(),
                    "results": list(queryset)}

        elif not page.has_next():
            return {"count": paginator.count,
                    "total_pages": paginator.num_pages,
                    "prev": page.previous_page_number(),
                    "next": None,
                    "results": list(queryset)}
        else:
            return {"count": paginator.count,
                    "total_pages": paginator.num_pages,
                    "prev": page.previous_page_number(),
                    "next": page.next_page_number(),
                    "results": list(queryset)}


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return self.object
