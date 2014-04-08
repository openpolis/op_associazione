from django.contrib import admin
from op_associazione.easycms.models import Page, Project, Dossier, DossierLink, PageAside, Banner
import models

# we define our resources to add to admin pages
class CommonMedia:
  js = (
    'https://ajax.googleapis.com/ajax/libs/dojo/1.6.0/dojo/dojo.xd.js',
    '/media/admin/js/editor.js',
  )
  css = {
    'all': ('/media/admin/css/editor.css',),
  }

class PageAsideInline(admin.StackedInline):
	model = PageAside
	extra = 2
	
class DossierLinkInline(admin.TabularInline):
	model = DossierLink
	extra = 2

class PageAdmin(admin.ModelAdmin):
	prepopulated_fields = { 'title_slug': ['title'] }
	list_display = ('title', 'title_slug', 'sub_title')
	fields = ['title', 'title_slug', 'sub_title', 'text', 'template']
	inlines = [PageAsideInline]
#	Media = CommonMedia

class ProjectAdmin(PageAdmin):
	list_display = ('title', 'order', 'order_link')
	fields = PageAdmin.fields + ['logo', 'url']

class DossierAdmin(PageAdmin):
	list_display = ('title', 'order', 'order_link')
	inlines = [PageAsideInline, DossierLinkInline]
	
class DossierLinkAdmin(admin.ModelAdmin):
	list_display = ('url', 'icon', 'order', 'order_link')
	
class PageAsideAdmin(admin.ModelAdmin):
	list_display = ('author', 'url', 'order', 'order_link')

class BannerAdmin(admin.ModelAdmin):
	list_display = ('name', 'link_url', 'background_image', 'updated_at', 'is_active')

admin.site.register(Page, PageAdmin) 
admin.site.register(PageAside, PageAsideAdmin) 
admin.site.register(Project, ProjectAdmin)
admin.site.register(Dossier, DossierAdmin)
admin.site.register(DossierLink, DossierLinkAdmin)
admin.site.register(Banner, BannerAdmin)

