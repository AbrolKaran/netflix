# Generated by Django 3.2.16 on 2022-12-03 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0011_movieproxy'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='movieproxy',
            options={'verbose_name': 'Movie', 'verbose_name_plural': 'Movies'},
        ),
    ]
