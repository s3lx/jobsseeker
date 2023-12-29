from rest_framework.serializers import ModelSerializer

from scraping.models import Language, Vacancy


class LanguageSerializer(ModelSerializer):

    class Meta:
        model = Language
        fields = ('name', 'slug')

        
class VacancySerializer(ModelSerializer):

    class Meta:
        model = Vacancy
        fields = ('__all__')
