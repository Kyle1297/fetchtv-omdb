# Generated by Django 3.2.4 on 2021-06-27 17:07

from django.db import migrations, models
import omdb.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('imdbID', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='IMDb ID')),
                ('title', models.CharField(db_index=True, max_length=255, verbose_name='Title')),
                ('type', models.CharField(choices=[('MOVIE', 'movie'), ('SERIES', 'series'), ('EPISODE', 'episode')], db_index=True, max_length=20, verbose_name='Type')),
                ('year', models.PositiveIntegerField(db_index=True, verbose_name='Year')),
            ],
        ),
    ]
