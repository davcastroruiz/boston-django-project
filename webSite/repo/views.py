from django.http import Http404
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, get_object_or_404, render_to_response
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import View
from .forms import UserForm, UrlForm
from .models import Site, Url
from HTMLParser import HTMLParser
import pycurl
import re
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO


results = {}
trashLinks = {}
headers = {}


class IndexView(generic.ListView):
    template_name = 'repo/index.html'
    context_object_name = 'all_s'

    def get_queryset(self):
        return Site.objects.all()


class ObtainHrefWithTag(HTMLParser):
        def __init__(self):
            HTMLParser.__init__(self)
            self.inLink = False
            self.dataArray = []
            self.countLanguages = 0
            self.lasttag = None
            self.lastname = None
            self.lastvalue = None
            self.value = None

        def handle_starttag(self, tag, attrs):
            self.inLink = True
            if tag == 'a':
                for name, value in attrs:
                    self.countLanguages += 1
                    self.inLink = True
                    self.lasttag = tag
                    # If href is defined, print it.
                    if name == "href":
                        self.value = value

        def handle_endtag(self, tag):
            if tag == "a":
                self.inlink = False

        def handle_data(self, data):
            if self.lasttag == 'a' and self.inLink and data.strip():
                options = ["Top", "By", "Date", "Up", "Name"]

                if options[0] in data or options[1] in data or options[2] in data or options[3] in data or options[4] in data:
                    trashLinks.update({data: self.value})
                else:
                    results.update({data: self.value})


class HREFSearchListView(generic.ListView):
    template_name = 'repo/detail_search.html'
    context_object_name = 'all_s'

    def get_queryset(self):
        results.clear()
        trashLinks.clear()
        query_string = self.request.GET.get('q')
        if query_string == '':
            query_string = "null"
        if query_string:
            buffer = BytesIO()
            c = pycurl.Curl()
            print query_string
            c.setopt(c.URL, query_string)
            c.setopt(c.WRITEFUNCTION, buffer.write)
            # Set our header function
            try:
                c.perform()
                c.close()
                encoding = None
                if 'content-type' in headers:
                    content_type = headers['content-type'].lower()
                    match = re.search('charset=(\S+)', content_type)
                    if match:
                        encoding = match.group(1)
                        print('Decoding using %s' % encoding)
                if encoding is None:
                    # Default encoding for HTML is iso-8859-1.
                    # Other content types may have different default encoding,
                    # or in case of binary data, may have no encoding at all.
                    encoding = 'iso-8859-1'
                    print('Assuming encoding is %s' % encoding)
                body = buffer.getvalue()
                # Decode using the encoding we figured out.
                # print(body.decode(encoding))
                parser = ObtainHrefWithTag()
                parser.feed(body.decode(encoding))
                print('\nUseful Links\n')


            except pycurl.error, error:
                errno, errstr = error
                print 'An error occurred: ', errstr
            # Figure out what encoding was sent with the response, if any.
            # Check against lowercased header name.

        return results


def detail(request, site_id):
    site = Site.objects.get(pk=site_id)
    results.clear()
    trashLinks.clear()
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, site.site_url)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    errorResults = {}
    # Set our header function
    try:
        c.perform()
        c.close()
        encoding = None
        if 'content-type' in headers:
            content_type = headers['content-type'].lower()
            match = re.search('charset=(\S+)', content_type)
            if match:
                encoding = match.group(1)
                print('Decoding using %s' % encoding)
        if encoding is None:
            # Default encoding for HTML is iso-8859-1.
            # Other content types may have different default encoding,
            # or in case of binary data, may have no encoding at all.
            encoding = 'iso-8859-1'
            print('Assuming encoding is %s' % encoding)
        body = buffer.getvalue()
        # Decode using the encoding we figured out.
        # print(body.decode(encoding))
        parser = ObtainHrefWithTag()
        parser.feed(body.decode(encoding))
        print('\nUseful Links\n')
        # for i in results:
        #     print i, "-->", results[i]
    except pycurl.error, error:
        errno, errstr = error
        print 'An error occurred: ', errstr
        errorResults = {'An error occurred: ', errstr}
        # Figure out what encoding was sent with the response, if any.
        # Check against lowercased header name.

    return render(request, 'repo/detail.html', {'all_s': results, 'site': site, 'error': errorResults})


class CreateSite(CreateView):
    model = Site
    fields = ['site_title', 'site_url']


class DetailView(generic.DetailView):
    model = Site
    template_name = 'repo/detail.html'


class UpdateViewType(generic.UpdateView):
    model = Site
    fields = ['site_title', 'site_url']


class DeleteViewType(DeleteView):
    model = Site
    success_url = reverse_lazy('repo:index')


class UrlToSiteCreate(CreateView):
    model = Url
    template_name = 'repo/site_form.html'
    fields = ['site', 'url_title', 'url']


class UpdateViewUrl(generic.UpdateView):
    model = Url
    form_class = UrlForm
    template_name = 'repo/site_form.html'

    def get_object(self, queryset=None):
        obj = Url.objects.get(id=self.kwargs['id'])
        return obj

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        self.request = request
        self.args = args
        self.kwargs = kwargs
        return handler(request, *args, **kwargs)


class DeleteUrl(DeleteView):
    model = Url

    def get_success_url(self):
        site = Url.objects.get(id=self.kwargs['id'])
        return reverse('repo:detail', kwargs={'pk': site.site_id})

    def get_object(self):
        site = Url.objects.get(id=self.kwargs['id'])
        return site


def SaveUrl(request):
    name = request.POST.get("url_name", "")
    url = request.POST.get("url_link", "")
    site_id = request.POST.get("url_site", "")
    site = get_object_or_404(Site, pk=site_id)

    def get_object(self):
        site = Url.objects.get(id=self.kwargs['id'])
        return site

    url_save = Url()
    url_save.site = site
    url_save.url = url
    url_save.url_title = name
    url_save.save()

    return render_to_response('repo/detail.html', {'site':site})
