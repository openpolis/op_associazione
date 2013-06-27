# Create your views here.

from django.http import HttpResponse, Http404
from django.template import  RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.cache import cache

from django import forms
from django.http import HttpResponseRedirect

from op_associazione.easycms.models import Page, PageAside, Project, Dossier
from django.conf import settings

import feedparser

class SearchForm(forms.Form):
    search = forms.CharField(max_length=30, min_length=3)

def search_result(request):
    from django.db.models import Q
    
    if request.method == 'POST' :
        form = SearchForm(request.POST)
        if form.is_valid() :
            # Process the data in form.cleaned_data
            results = Page.objects.filter(Q(text__icontains=form.cleaned_data['search']) | Q(title__icontains=form.cleaned_data['search']))
            return render_to_response('easycms/search_result.html', {
                'search_text' : form.cleaned_data['search'],
                'search_results' : results
            }, context_instance=RequestContext(request))
    return HttpResponseRedirect('/')     
    


def page(request, page_slug=None):
    try:
        page = Page.objects.get(title_slug=page_slug)
    except Page.DoesNotExist:
        raise Http404 
    template = 'page'
    if ( page.template != 'default' ):
        template = 'easycms/' + page.template + '.html'
    return render_to_response( template ,     {
            'page_slug' : page_slug,
            'page' : page,
            'asides' : page.asides.all()
        },context_instance=RequestContext(request))


def homepage(request):
    # feeds are extracted and cached for one hour (memcached)
    feeds = cache.get('op_associazione_home_feeds')

    if feeds is None:
        feeds = {}
        feeds['blog'] = feedparser.parse(settings.OP_BLOG_FEED)
        feeds['tw'] = feedparser.parse(settings.OP_TW_FEED)
        feeds['fb'] = feedparser.parse(settings.OP_FB_FEED)
        cache.set('op_associazione_home_feeds', feeds, 3600)

    return render_to_response('easycms/home.html', 
      {'blog_entries': feeds['blog'].entries[0:5],
       'tw_entries': feeds['tw'].entries[0:3],
       'fb_entries': feeds['fb'].entries[0:3]}, 
      context_instance=RequestContext(request))


def dossier( request, page_slug=None ):
    page = get_object_or_404(Dossier, title_slug=page_slug)
    return render_to_response('easycms/dossier.html',     {
            'page_slug' : page_slug,
            'page' : page,
            'asides' : page.asides.all()
        },context_instance=RequestContext(request))

def project( request, page_slug ):
    page = get_object_or_404(Project, title_slug=page_slug)
    # feeds are extracted and cached for one hour (memcached)
    feed = cache.get('op_associazione_buzz_feed')
    if feed is None:
        feed = feedparser.parse(settings.BUZZ_FEED)
        cache.set('op_associazione_buzz_feed', feed, 3600)
    
    return render_to_response('easycms/project.html',     {
            'buzz_feed': feed.entries[0:5],
            'page_slug': page_slug,
            'page': page,
            'asides': page.asides.all()
        },context_instance=RequestContext(request))
