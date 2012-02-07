# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models

class Membership(models.Model):
    MEMBER_TYPE = (
        ('fondatore', 'Socio fondatore'),
        ('sostenitore', 'Socio sostenitore'),
        ('ordinario', 'Socio ordinario'),
        ('studente', 'Socio studente')
    )
    type_of_membership     = models.CharField("Tipo di iscrizione",max_length=50,choices=MEMBER_TYPE, default='ordinario', help_text="Seleziona il tipo di iscrizione")
    fee                    = models.IntegerField("Quota (euro)", help_text="Inserisci la quota che vuoi versare. Considera le quote minime: Ordinario: 50€ Sostenitore: 500€ Studente/Precario: 20€.")
    payed                  = models.IntegerField("Quota pagata",null=True, blank=True)
    payed_at               = models.DateField("Data pagamento",null=True, blank=True)
    expire_at              = models.DateField("Scadenza",null=True, blank=True)
    sent_card_at           = models.DateField("Data invio",null=True, blank=True)
    notes                  = models.TextField("Note", blank=True)
    is_active              = models.BooleanField("Attivato", default=False)
    associate              = models.ForeignKey('Associate')
    public_subscription    = models.BooleanField("Iscrizione pubblica",default=False, help_text='Voglio comparire tra i sostenitori dell\'associazione e desidero che la mia quota di sottoscrizione sia pubblicata insieme al mio nome')
    created_at             = models.DateField(auto_now_add=True)
    updated_at             = models.DateField(auto_now=True)

    @staticmethod
    def get_minimum_fee(member_type):
        if member_type == 'sostenitore':
            return 500
        if member_type == 'ordinario':
            return 50
        if member_type == 'studente':
            return 10
            
    @staticmethod
    def get_typename(member_type):
        for entry in Membership.MEMBER_TYPE:
            if entry[0] == member_type:
                return entry[1]
        return u'Tipologia di utente %s non trovata' % member_type

    def __unicode__(self):
        return "%s at %s" % (self.associate, self.created_at.isoformat())

    class Meta:
        verbose_name = 'Iscrizione'
        verbose_name_plural = 'Iscrizioni'

class Associate(models.Model):
    GENDERS = (
        ('M', 'Uomo'),
        ('F', 'Donna'),
    )
    
    first_name            = models.CharField('Nome',max_length=200)
    last_name             = models.CharField('Cognome',max_length=200)
    birth_date            = models.DateField('Data di nascita')
    gender                = models.CharField('Sesso',max_length=1, choices=GENDERS, null=False, blank=False)
    fiscal_code           = models.CharField('Codice fiscale',max_length=20, help_text="Inserisci codice fiscale (16 caratteri)")
    phone_number          = models.CharField('Telefono',max_length=200,blank=True, null=True)
    wants_newsletter      = models.BooleanField('Newsletter',help_text='Voglio ricevere la newsletter via email')
    email                 = models.EmailField(unique=True)
    street                = models.CharField('Via, viale, ecc', max_length=200)
    civic_nb              = models.CharField('Numero civico', max_length=20)
    zip_code              = models.CharField('CAP', max_length=20)
    location              = models.CharField('Città', max_length=100)
    province              = models.CharField('Provincia', max_length=100)
    country               = models.CharField('Nazione', max_length=100)
    exp_street            = models.CharField('Via, viale, ecc', max_length=200)
    exp_civic_nb          = models.CharField('Numero civico', max_length=20)
    exp_zip_code          = models.CharField('CAP', max_length=20)
    exp_location          = models.CharField('Città', max_length=100)
    exp_province          = models.CharField('Provincia', max_length=100)
    exp_country           = models.CharField('Nazione', max_length=100)
    hash_key              = models.CharField('HASH', max_length=40)
    created_at            = models.DateField(auto_now_add=True)
    updated_at            = models.DateField(auto_now=True)

    @property
    def memberships(self):
        return self.membership_set.all()

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        verbose_name = 'Associato'
        verbose_name_plural = 'Associati'

class Citizen(Associate):
    class Meta:
        verbose_name = 'Cittadino'
        verbose_name_plural = 'Cittadini'
    
class Organization(Associate):
    ORG_TYPE = (
        ('no-profit', 'No profit'),
        ('profit', 'Profit'),
        ('pa', 'Pubblica Amministrazione'),
        ('other', 'Altro'),
    )
    denomination             = models.CharField('Denominazione',max_length=300)
    type_of_organization     = models.CharField('Tipo di Organizzazione',max_length=100, choices=ORG_TYPE)
    vat_code                 = models.CharField('Partita Iva',max_length=100, help_text="Inserire il codice di 11 cifre, privo dell'identificativo nazionale")
    #    location_address         = models.OneToOneField(Address, related_name='+')

    def __unicode__(self):
        if self.denomination is not None and self.denomination != "":
            return self.denomination
        else:
            return super(Organization, self).__unicode__()

    class Meta:
        verbose_name = 'Organizzazione'
        verbose_name_plural = 'Organizzazioni'

class Politician(Associate):
    charge             = models.TextField('Incarichi', blank=True, null=True)
    public_revenue     = models.BooleanField('Redditi online', help_text='In quanto socio di openpolis con funzioni politiche, m\'impegno a fornire annualmente all\'Associazione openpolis la mia dichiarazione dei redditi, lo stato patrimoniale e le spese elettorali come previsto dalla legge 5 luglio 1982 n. 441, affinché  l\'associazione si occupi, direttamente o indirettamente, della pubblicazione in internet delle dichiarazioni stesse, senza alcuna limitazione.')

    class Meta:
        verbose_name = 'Politico'
        verbose_name_plural = 'Politici'

# url: http://djangosnippets.org/snippets/998/
class OrderedModel(models.Model):
    order = models.PositiveIntegerField(editable=False)

    def save(self):
        if not self.id:
            try:
                self.order = self.__class__.objects.all().order_by("-order")[0].order + 1
            except IndexError:
                self.order = 0
        super(OrderedModel, self).save()
        

    def order_link(self):
        model_type_id = ContentType.objects.get_for_model(self.__class__).id
        model_id = self.id
        kwargs = {"direction": "up", "model_type_id": model_type_id, "model_id": model_id}
        url_up = reverse("admin-move", kwargs=kwargs)
        kwargs["direction"] = "down"
        url_down = reverse("admin-move", kwargs=kwargs)
        return '<a href="%s">up</a> | <a href="%s">down</a>' % (url_up, url_down)
    order_link.allow_tags = True
    order_link.short_description = 'Move'
    order_link.admin_order_field = 'order'


    @staticmethod
    def move_down(model_type_id, model_id):
        try:
            ModelClass = ContentType.objects.get(id=model_type_id).model_class()

            lower_model = ModelClass.objects.get(id=model_id)
            higher_model = ModelClass.objects.filter(order__gt=lower_model.order)[0]
            
            lower_model.order, higher_model.order = higher_model.order, lower_model.order
            
            higher_model.save()
            lower_model.save()
            
        except IndexError:
            pass
        except ModelClass.DoesNotExist:
            pass
                
    @staticmethod
    def move_up(model_type_id, model_id):
        try:
            ModelClass = ContentType.objects.get(id=model_type_id).model_class()

            higher_model = ModelClass.objects.get(id=model_id)
            lower_model = ModelClass.objects.filter(order__lt=higher_model.order)[0]

            lower_model.order, higher_model.order = higher_model.order, lower_model.order

            higher_model.save()
            lower_model.save()
        except IndexError:
            pass
        except ModelClass.DoesNotExist:
            pass

    class Meta:
        ordering = ["order"]
        abstract = True