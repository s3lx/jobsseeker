# Generated by Django 4.1.2 on 2022-10-25 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='city',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='scraping.city', verbose_name='Город'),
        ),
    ]
