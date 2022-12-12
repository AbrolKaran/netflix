from re import template
from telnetlib import DET
from django.http import Http404
from django.views.generic import ListView, DeleteView
from django.utils import timezone
from neflix.db.models import PublishStateOptions
# Create your views here.
from .models import Playlist, MovieProxy, TVShowProxy, TVShowSeasonProxy

class PlaylistMixin():
    template_name = 'playlist_list.html'
    title = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(* args, **kwargs)
        if self.title is not None:
            context['title'] = self.title
        
        print(context)
        return context

    def get_queryset(self):
        return super().get_queryset().published()


class MovieListView(PlaylistMixin, ListView):
    queryset = MovieProxy.objects.all()
    title = "Movies"

class MovieDetailView(PlaylistMixin, DeleteView):
    template_name = 'playlists/movie_detail.html'
    queryset = MovieProxy.objects.all()

class PlaylistDetailView(PlaylistMixin, DeleteView):
    template_name = 'playlists/playlist_detail.html'
    queryset = Playlist.objects.all()


class TVShowDetailView(PlaylistMixin, DeleteView):
    template_name = 'playlists/tvshow_detail.html'
    queryset = TVShowProxy.objects.all()


class TVShowSeasonDetailView(PlaylistMixin, DeleteView):
    template_name = 'playlists/season_detail.html'
    queryset = TVShowSeasonProxy.objects.all()

    def get_object(self):
        kwargs = self.kwargs
        show_slug = kwargs.get("showSlug")
        season_slug = kwargs.get("seasonSlug")
        now = timezone.now()
        try:
            obj = TVShowSeasonProxy.objects.get(state =PublishStateOptions.PUBLISH, publish_timestamp__lte=now,parent__slug_iexact = show_slug, slug__iexact =season_slug)
        except TVShowSeasonProxy.MultipleObjectsReturned:
            qs = TVShowSeasonProxy.objects.filter(parent__slug_iexact = show_slug, slug__iexact =season_slug).published()
            obj = qs.first()
            # log this
        except:
            raise Http404
        return obj

class TVShowListView(PlaylistMixin, ListView):
    queryset= TVShowProxy.objects.all()
    title = "TV Shows"


class FeaturedPlaylistListView(PlaylistMixin, ListView):
    queryset= Playlist.objects.featured_playlists()
    title = "Featured"