from django.template import RequestContext
from django.core.urlresolvers import resolve
from op_associazione.easycms.models import Project

def navigation(request):
    return {
        'projects' : Project.objects.all(),
		'current_route_name' : resolve(request.get_full_path()).url_name
    }