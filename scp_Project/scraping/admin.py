from django.contrib import admin
from .models import Language, Vacancy, Error, Url

admin.site.register(Language)
admin.site.register(Vacancy)
admin.site.register(Error)
admin.site.register(Url)