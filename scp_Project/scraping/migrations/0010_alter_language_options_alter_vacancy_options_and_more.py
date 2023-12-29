# Generated by Django 4.1.3 on 2022-12-14 11:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0009_alter_url_url_data'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='language',
            options={'verbose_name': 'Programming language', 'verbose_name_plural': 'Programming languages'},
        ),
        migrations.AlterModelOptions(
            name='vacancy',
            options={'ordering': ['-timestamp'], 'verbose_name': 'Job', 'verbose_name_plural': 'Jobs'},
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Programming language'),
        ),
        migrations.AlterField(
            model_name='url',
            name='language',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='scraping.language', verbose_name='Programming language'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='company',
            field=models.CharField(max_length=250, verbose_name='Company'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='description',
            field=models.TextField(verbose_name='Job description'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='language',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='scraping.language', verbose_name='Programming language'),
        ),
        migrations.AlterField(
            model_name='vacancy',
            name='title',
            field=models.CharField(max_length=250, verbose_name='Job Title'),
        ),
    ]
