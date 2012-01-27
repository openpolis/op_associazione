# Create your views here.

from django.http import HttpResponse, Http404
from op_associazione.easycms.models import Page, PageAside, Project, Dossier
from django.template import  RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from django import forms
from django.http import HttpResponseRedirect

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
		return render_to_response('easycms/home.html', {},context_instance=RequestContext(request))
	template = 'page'
	if ( page.template != 'default' ):
		template = 'easycms/' + page.template + '.html'
	return render_to_response( template , 	{
			'page_slug' : page_slug,
			'page' : page,
			'asides' : page.asides.all()
		},context_instance=RequestContext(request))


def dossier( request, page_slug=None ):
	page = get_object_or_404(Dossier, title_slug=page_slug)
	return render_to_response('easycms/dossier.html', 	{
			'page_slug' : page_slug,
			'page' : page,
			'asides' : page.asides.all()
		},context_instance=RequestContext(request))

def project( request, page_slug ):
	page = get_object_or_404(Project, title_slug=page_slug)
	return render_to_response('easycms/project.html', 	{
			'page_slug' : page_slug,
			'page' : page,
			'asides' : page.asides.all()
		},context_instance=RequestContext(request))