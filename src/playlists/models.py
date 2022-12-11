from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import Avg, Max, Min
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.text import slugify
# Create your models here.
from neflix.db.models import PublishStateOptions
from neflix.db.receivers import publish_state_pre_save, slugify_pre_save
from categories.models import Category
from ratings.models import Rating
from tags.models import TaggedItem
from videos.models import Video

class PLaylistQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state=PublishStateOptions.PUBLISH,
            publish_timestamp__lte= now 
        )

class PlaylistManager(models.Manager):
    def get_queryset(self):
        return PLaylistQuerySet(self.model, using=self._db)

    def published(self):
        return self.get_queryset().published()

class Playlist(models.Model):
    class PlaylistTypeChoices(models.TextChoices):
        MOVIE = 'MOV', "Movie"
        SHOW = 'TVS', "TV Show"
        SEASON = 'SEA', "Season"
        PLAYLIST = 'PLY', "Playlist"
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category,related_name='playlists', blank = True, null =True, on_delete = models.SET_NULL)
    order = models.IntegerField(default=1) 
    title = models.CharField(max_length=220)
    type = models.CharField(max_length=3, choices=PlaylistTypeChoices.choices,default=PlaylistTypeChoices.PLAYLIST)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, null=True) 
    video = models.ForeignKey(Video, related_name='playlist_featured', blank=True, null=True, on_delete=models.SET_NULL)
    # videos = models.ManyToManyField(Video, related_name='playlist_item', blank=True)
    active = models.BooleanField(default=True)  
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=2, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    tags = GenericRelation(TaggedItem, related_query_name='playlist')
    ratings = GenericRelation(Rating, related_query_name='playlist')
    objects = PlaylistManager()

    def __str__(self):
        return self.title
    
    def get_rating_avg(self):
        return Playlist.objects.filter(id=self.id).aggregate(Avg("ratings__value"))

    def get_rating_spread(self):
        return Playlist.objects.filter(id=self.id).aggregate(max = Max("ratings__value"), min = Min("ratings__value"))

    @property
    def is_published(self):
        if self.active is False:
            return False
        state = self.state
        if state != PublishStateOptions.PUBLISH:
            return False
        pub_timestamp = self.publish_timestamp
        if pub_timestamp is None:
            return False
        now = timezone.now()
        return pub_timestamp <= now

    # def get_playlist_ids(self):
    #     # self.<foreigned_obj>_set.all()
    #     return list(self.playlist_featured.all().values_list('id', flat=True))
pre_save.connect(publish_state_pre_save, sender=Playlist)
pre_save.connect(slugify_pre_save, sender=Playlist)


class MovieProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(type=Playlist.PlaylistTypeChoices.MOVIE)

class MovieProxy(Playlist):

    objects = MovieProxyManager()

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        proxy = True

    def save(self,*args,**kwargs):
        self.type = Playlist.PlaylistTypeChoices.MOVIE
        super().save(*args,**kwargs)

class TVShowProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=True, type=Playlist.PlaylistTypeChoices.SHOW)

class TVShowProxy(Playlist):

    objects = TVShowProxyManager()

    class Meta:
        verbose_name = 'TV Show'
        verbose_name_plural = 'TV Shows'
        proxy = True

    def save(self,*args,**kwargs):
        self.type = Playlist.PlaylistTypeChoices.SHOW
        super().save(*args,**kwargs)

class TVShowSeasonProxyManager(PlaylistManager):
    def all(self):
        return self.get_queryset().filter(parent__isnull=False, type=Playlist.PlaylistTypeChoices.SEASON)

class TVShowSeasonProxy(Playlist):

    objects = TVShowSeasonProxyManager()
    
    class Meta:
        verbose_name = 'Season'
        verbose_name_plural = 'Seasons'
        proxy = True

    def save(self,*args,**kwargs):
        self.type = Playlist.PlaylistTypeChoices.SEASON
        super().save(*args,**kwargs)

class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-timestamp']

