# Generated by Django 3.2.16 on 2022-12-03 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0004_alter_playlist_video'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlist',
            name='videos',
        ),
    ]
