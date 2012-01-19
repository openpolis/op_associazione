from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'op_associazione.views.home', name='home'),
    # url(r'^op_associazione/', include('op_associazione.foo.urls')),

	# url(r'^page/(?P<page_slug>\S*)$', 'op_associazione.easycms.views.page'),
	url(r'^', include('op_associazione.easycms.urls')),
	
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/Users/daniele/Workspace/op_associazione/web/media'}),
	
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

	url(r'^admin/orderedmove/(?P<direction>up|down)/(?P<model_type_id>\d+)/(?P<model_id>\d+)/$', 'op_associazione.views.admin_move_ordered_model', name="admin-move"),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

