# Generated by Django 3.2.16 on 2022-12-03 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_video_publish_timestamp_video_state_video_timestamp_and_more'),
        ('playlists', '0005_remove_playlist_videos'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaylistItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=1)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('playlist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playlists.playlist')),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='videos.video')),
            ],
            options={
                'ordering': ['order', '-timestamp'],
            },
        ),
    ]
