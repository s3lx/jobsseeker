import datetime
from rest_framework import filters
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import *

period = datetime.date.today() - datetime.timedelta(1)

class DateFilterBackend(filters.BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        language_slug = request.query_params.get('language', None)
        return queryset.filter(
            language__slug=language_slug,
            timestamp__gte=period)


class LanguageViewSet(ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class VacancyViewSet(ModelViewSet):
    queryset = Vacancy.objects.all()
    serializer_class = VacancySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        language_slug = self.request.query_params.get('language', None)
        qs = None
        if language_slug:
            language = Language.objects.filter(slug=language_slug).first()
            if language:
                qs = Vacancy.objects.filter(language=language,timestamp__gte=period)
        self.queryset = qs
        return self.queryset
