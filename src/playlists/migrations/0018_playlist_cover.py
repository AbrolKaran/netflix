# Generated by Django 3.2.16 on 2022-12-13 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('covers', '0002_alter_cover_field_name'),
        ('playlists', '0017_alter_playlist_related'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='cover',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='covers.cover'),
        ),
    ]