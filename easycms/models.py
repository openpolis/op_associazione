import datetime
from django.db import models
from op_associazione.models import OrderedModel
from markdown import markdown


class Page(OrderedModel):
    title         = models.CharField('Titolo', max_length=200)
    title_slug    = models.SlugField(unique=True, help_text="Il valore e' generato automaticamente dal titolo. Deve essere univoco.")
    sub_title    = models.CharField('Sotto-Titolo', max_length=200, blank=True)
    text         = models.TextField('Contenuto')
    text_html     = models.TextField('Contenuto HTML')
    template    = models.CharField('Layout',max_length=20, default='page')
    
    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return '/' + self.title_slug
        
    def save(self):
            self.text_html = markdown(self.text)
            super(Page, self).save()
    
    class Meta(OrderedModel.Meta):
        verbose_name = "Pagina"
        verbose_name_plural = "Pagine"

class PageAside(OrderedModel):
    text        = models.TextField('Text')
    author        = models.CharField('Author', max_length=200, blank=True)
    url            = models.CharField('Url', max_length=300, blank=True)
    page        = models.ForeignKey(Page, related_name='asides')
    def __unicode__(self):
        return self.author
    
    class Meta(OrderedModel.Meta):
        verbose_name = "Contenuto in spalla"
        verbose_name_plural = "Contenuti in spalla"

class Project(Page):
    logo        = models.ImageField(blank=True, upload_to='img/' )  
    url         = models.CharField('Url', max_length=300, blank=True)
    
    def get_absolute_url(self):
        return '/progetti/%s' % self.title_slug
    
    def save(self):
            self.text_html = markdown(self.text)
            super(Project, self).save()
    
    class Meta(OrderedModel.Meta):
        verbose_name = "Progetto"
        verbose_name_plural = "Progetti"
    
class Dossier(Page):
    
    def get_absolute_url(self):
        return '/dossier/%s' % self.title_slug
        
    def save(self):
            self.text_html = markdown(self.text)
            super(Dossier, self).save()
    
class DossierLink(OrderedModel):
    GREEN_ICON = 'download'
    BLUE_ICON = 'forward'
    ICON_CHOICES = (
        ( GREEN_ICON , 'Download' ),
        ( BLUE_ICON , 'Link')
    )
    
    url            = models.URLField(verify_exists=True)
    icon        = models.CharField(choices=ICON_CHOICES, default=GREEN_ICON, max_length=20 )
    text        = models.CharField('Link Text', max_length=200)
    dossier        = models.ForeignKey(Dossier, related_name='links')
    
    class Meta(OrderedModel.Meta):
        verbose_name = "Risorsa Dossier"
        verbose_name_plural = "Risorse Dossier"
        