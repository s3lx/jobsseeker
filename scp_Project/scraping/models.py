from django.db import models
from .utils import from_cyrillic_to_eng


def default_urls():
    return {"get_parse": ""}


class Language(models.Model):

    name = models.CharField(max_length=50, verbose_name='Programming language',unique=True)
    slug = models.CharField(max_length=50,blank=True, unique=True)

    class Meta:
        verbose_name = 'Programming language'
        verbose_name_plural = 'Programming languages'

    def __str__(self):
        return self.name

    def save(self, *args,**kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_eng(str(self.name))
        super().save(*args,**kwargs)

class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name='Job Title')
    company = models.CharField(max_length=250, verbose_name='Company')
    description = models.TextField(verbose_name='Job description')
    language = models.ForeignKey('Language',on_delete=models.CASCADE, verbose_name='Programming language',blank=True)
    timestamp = models.DateField(auto_now_add=True,blank=True)


    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        ordering = ['-timestamp']

    def __str__(self):
        return self.title

class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = models.JSONField()

    def __str__(self):
        return str(self.timestamp)

class Url(models.Model):
    language = models.ForeignKey('Language',on_delete=models.CASCADE, verbose_name='Programming language',blank=True)
    url_data = models.JSONField(default=default_urls)

    class Meta:
        unique_together = ("language",)


