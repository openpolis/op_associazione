#from django.conf.urls.defaults import patterns, include, url
from django.conf.urls import patterns, url, include
from op_associazione.easycms.models import Dossier
from django.views.generic import DetailView, ListView

urlpatterns = patterns('op_associazione.easycms.views',
    
    url(r'^ricerca/$', 'search_result'),
    url(r'^progetti/(?P<page_slug>[-\w]+)/$',     'project',         name='progetti'),
    url(r'^dossier/(?P<page_slug>[-\w]+)/$', 'dossier', name='dossier'),
    url(r'^chi-siamo/$', 'page', {'page_slug': 'chi-siamo'}, name="about-us"),
    url(r'^home-preview/$', 'homepage', {'preview': True}),
    url(r'^(?P<page_slug>[-\w]+)/$', 'page', name='generic-page'),
    url(r'^$', 'homepage', {}),
)