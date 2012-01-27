from django.template import RequestContext
from django.core.urlresolvers import resolve
from op_associazione.easycms.models import Project, Dossier

def navigation(request):
	return {
        'projects' : Project.objects.all(),
		'dossiers' : Dossier.objects.all(),
		'current_route_name' : resolve(request.path).url_name
    }