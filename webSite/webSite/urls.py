"""webSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # include the login and logout views from django
    url(r'^accounts/login/$', auth_views.login, {'template_name': 'registration/login.html'}, name='login'),
    # index website
    url(r'', include('repo.urls')),
    url(r'^logout/$', auth_views.logout, {'next_page': '/accounts/login'}, name='logout'),
    # add a new app in the website
    url(r'^music/', include('music.urls')),
    # urls for reset and functions
    url(r'^accounts/password_reset/$', auth_views.password_reset, {'template_name': 'registration/password_reset_form.html'}, name='password_reset'),
    # reset done will need another html template
    url(r'^accounts/password_reset/done/$', auth_views.password_reset_done, {'template_name': 'registration/password_reset_form.html'}, name='password_reset_done'),
    url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, {'template_name': 'registration/password_reset_form.html'}, name='password_reset_confirm'),
    url(r'^accounts/reset/done/$', auth_views.password_reset_complete,{'template_name': 'registration/password_reset_form.html'},  name='password_reset_complete'),
    # url for change and functions
    url(r'^accounts/password_change/$', login_required(auth_views.password_change), {'template_name': 'registration/password_reset_form.html'}, name='password_change'),
    # template success text
    url(r'^accounts/password_change/done/$', login_required(auth_views.password_change_done), {'template_name': 'registration/password_reset_form.html'}, name='password_change_done'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
