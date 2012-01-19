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
	if request.method == 'POST' :
		form = SearchForm(request.POST)
		if form.is_valid() :
			# Process the data in form.cleaned_data
			results = Page.objects.filter(text__icontains=form.cleaned_data['search'])
			return render_to_response('easycms/search_result.html', {
				'search_text' : form.cleaned_data['search'],
				'search_results' : results
			}, context_instance=RequestContext(request))
	return HttpResponseRedirect('/')	 
	

def page(request, page_slug=None):
	try:
		page = Page.objects.get(title_slug=page_slug)
	except Page.DoesNotExist:
		return render_to_response('easycms/home.html', {
			
		},context_instance=RequestContext(request))
#		raise Http404
#	page = get_object_or_404(Page, title_slug=page_slug)
	return render_to_response('easycms/page.html', 	{
			'page_slug' : page_slug,
			'page' : page,
			'asides' : page.asides.all()
		},context_instance=RequestContext(request))
#	t = loader.get_template('easycms/page.html')
#	c = Context({
#		'page_slug' : page_slug,
#		'page' : page,
#		'asides' : page.asides.all()
#	})
#	return HttpResponse(t.render(c))

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