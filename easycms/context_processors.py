from django.template import RequestContext
from django.core.urlresolvers import resolve, Resolver404
from django.http import Http404
from op_associazione.easycms.models import Project, Dossier

def navigation(request):
    
    try:
        current_route_name = resolve(request.path).url_name
    except Resolver404:
        current_route_name = ''
        
    return {
        'projects' : Project.objects.all(),
        'dossiers' : Dossier.objects.all(),
        'current_route_name' : current_route_name
    }