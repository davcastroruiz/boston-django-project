# # 1from django.http import Http404
# # 1from django.http import HttpResponse
# # 1from django.template import loader
# from django.shortcuts import render, get_object_or_404
from .models import Album, Song
#
#
# def index(request):
#     all_albums = Album.objects.all()
#     # 1template = loader.get_template('music/index.html')
#     context = {'all_albums': all_albums}
#     # 1return HttpResponse(template.render(context, request))
#     return render(request, 'music/index.html', context)
#
#
# def detail(request, album_id):
#     # 1return HttpResponse("<h2>Details for Album id: " + str(album_id) + "</h2>")
#     #   1try:
#     #   1album = Album.objects.get(pk=album_id)
#     #   1except Album.DoesNotExist:
#     #    1raise Http404("Album does not exist")
#     album = get_object_or_404(Album, pk=album_id)
#     return render(request, 'music/detail.html', {'album': album})
#
#
# def favorite(request, album_id):
#     album = get_object_or_404(Album, pk=album_id)
#     try:
#         selected_song = album.song_set.get(pk=request.POST["song"])
#     except (KeyError, Song.DoesNotExist):
#         return render(request, 'music/detail.html', {
#             'album': album,
#             'error_message': "You did not select a valid song"
#         })
#     else:
#         for song in album.song_set.all():
#             song.is_favorite = False
#             song.save()
#
#         selected_song.is_favorite = True
#         selected_song.save()
#         return render(request, 'music/detail.html', {'album': album})
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm
import re
import operator
from django.db.models import Q


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:

        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']

    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)]


def create_query(query_string, search_fields):
    terms = normalize_query(query_string)
    query = reduce(operator.and_, [reduce(operator.or_, [Q(**{"%s__icontains" % f: t}) for f in search_fields]) for t in terms])

    return query


class AlbumSearchListView(generic.ListView):
    """
    Display a Blog List page filtered by the search query.

    """
    template_name = 'music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        query_string = self.request.GET.get('q')
        if query_string == '':
            query_string = "null"
        if query_string:
            entry_query = create_query(query_string, ['album_title', 'artist', 'genre',  'id' ])

            result = Album.objects.filter(entry_query)

        return result


class SongSearchListView(generic.ListView):
    """
    Display a Blog List page filtered by the search query.

    """
    template_name = 'music/detail_songs.html'
    context_object_name = 'all_songs'

    def get_queryset(self):
        query_string = self.request.GET.get('q')
        if query_string == '':
            query_string = "null"
        if query_string:
            entry_query = create_query(query_string, ['song_title', 'file_type'])

            result = Song.objects.filter(entry_query)

        return result


class IndexView(generic.ListView):
    template_name = 'music/index.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return Album.objects.all()


class DetailView(generic.DetailView):
    model = Album
    template_name = 'music/detail.html'


class DetailSongsView(generic.ListView):
    template_name = 'music/detail_songs.html'
    context_object_name = 'all_songs'

    def get_queryset(self):
        return Song.objects.all()


class AlbumCreate(CreateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']


class AlbumUpdate(UpdateView):
    model = Album
    fields = ['artist', 'album_title', 'genre', 'album_logo']


class AlbumDelete(DeleteView):
    model = Album
    success_url = reverse_lazy('music:index')


class SongDelete(DeleteView):
    model = Song
    success_url = reverse_lazy('music:songs')


class SongCreate(CreateView):
    model = Song
    fields = ['album', 'song_title', 'file_type', 'is_favorite']


class SongCreateFromSong(CreateView):
    model = Song
    fields = ['album', 'song_title', 'file_type', 'is_favorite']
    success_url = reverse_lazy('music:songs')


class UserFormView(View):
    form_class = UserForm
    template_name = 'music/registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()

            # cleaned (normalized) data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('music:index')
        return render(request, self.template_name, {'form': form})