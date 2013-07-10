from django.conf.urls.defaults import patterns, include, url

# Aministration
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^(?P<page_slug>statuto|privacy|campagne|eng|bilancio)/','op_associazione.views.static_page', name='static-page'),
    # url(r'^5xmille/$', TemplateView.as_view(template_name='statics/5xmille.html'), name="5xmille"),
    url(r'^5xmille/$', 'op_associazione.views.cinquexmille', name="5xmille"),

    # Subscribe urls
    url(r'^sostienici/(?P<member_type>politico|cittadino|organizzazione)/$', 'op_associazione.views.subscribe_module', {}, name="subscribe-module"),
    url(r'^sostienici/completa-associazione/$', 'op_associazione.views.payment', {}, name="subscribe-pay"),
    url(r'^sostienici/$', 'op_associazione.views.subscribe', {}, name="subscribe"),
    url(r'^sostienici/(?P<page_slug>dona|collabora)/$','op_associazione.views.static_page', name='subscribe-other'),
    url(r'^rinnovo-iscrizione/(?P<user_hash>[-\w]+)/$', 'op_associazione.views.renewal', {}, name="subscribe-renewal"),
    url(r'^rinnovo-iscrizione/', 'op_associazione.views.renewal_request', {}, name="subscribe-renewal-request"),

    (r'^qrcode/$', lambda x: HttpResponseRedirect('/')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # Ordering models
    url(r'^admin/orderedmove/(?P<direction>up|down)/(?P<model_type_id>\d+)/(?P<model_id>\d+)/$', 'op_associazione.views.admin_move_ordered_model', name="admin-move"),

    # EasyCMS urls
    url(r'^', include('op_associazione.easycms.urls')),
    
)

