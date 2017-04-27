from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'music'
urlpatterns = [
    # /music/
    url(r'^$', views.IndexView.as_view(), name='index'),
    # /music/songs
    url(r'^songs/$', views.DetailSongsView.as_view(), name='songs'),
    # # /music/songs/id
    url(r'songs/(?P<pk>[0-9]+)/delete/$', login_required(views.SongDelete.as_view()), name='song-delete'),
    # /music/
    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    # /music/id/
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # # /music/id/favorite
    # url(r'^(?P<album_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    # # /music/album/add/
    url(r'album/add/$', login_required(views.AlbumCreate.as_view()), name='album-add'),
    # # /music/album/id/delete
    url(r'album/(?P<pk>[0-9]+)/delete/$', login_required(views.AlbumDelete.as_view()), name='album-delete'),
    # # /music/album/id/newSong
    url(r'album/(?P<pk>[0-9]+)/newSong/$', login_required(views.SongCreate.as_view()), name='song-add'),
    # # /music/album/id/delete
    url(r'songs/newSong/$', login_required(views.SongCreateFromSong.as_view()), name='songs-songs-add'),
    # # /music/album/id/
    url(r'album/(?P<pk>[0-9]+)/$', login_required(views.AlbumUpdate.as_view()), name='album-update'),
    # album_search_list_view
    url(r'^search/$', views.AlbumSearchListView.as_view(), name='search_list_view'),
    # song_search_list_view
    url(r'^search/song/$', views.SongSearchListView.as_view(), name='music_search_list_view'),

]
