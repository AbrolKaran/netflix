# Generated by Django 3.2.16 on 2022-12-13 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playlists', '0016_alter_playlist_related'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='related',
            field=models.ManyToManyField(blank=True, related_name='_playlists_playlist_related_+', through='playlists.PlaylistRelated', to='playlists.Playlist'),
        ),
    ]