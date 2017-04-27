from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'repo'


urlpatterns = [
    # /repo/
    url(r'^$', login_required(views.IndexView.as_view()), name='index'),
    # search_list_view HREF
    url(r'^search/$', views.HREFSearchListView.as_view(), name='search_list_view'),
    # add site
    url(r'^add/$', login_required(views.CreateSite.as_view()), name='site-add'),
    # view details
    url(r'^site/(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # view details search
    url(r'^site/search/(?P<site_id>[0-9]+)/$', views.detail, name='search_list_view_site'),
    url(r'^site/add/in_site/$', views.SaveUrl, name='add_in_site'),

    # view update site
    url(r'^site/update/(?P<pk>[0-9]+)/$', login_required(views.UpdateViewType.as_view()), name='site-update'),
    url(r'^site/update_url/(?P<id>\d+)/$', login_required(views.UpdateViewUrl.as_view()), name='urlupdate'),
    url(r'^site/delete_url/(?P<id>\d+)/$', login_required(views.DeleteUrl.as_view()), name='urldelete'),
    # view delete site
    url(r'^delete/(?P<pk>[0-9]+)/$', login_required(views.DeleteViewType.as_view()), name='type-delete'),
    url(r'^site/add/$', login_required(views.UrlToSiteCreate.as_view()), name='url-add'),
]