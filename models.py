# url: http://djangosnippets.org/snippets/998/
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models

#from os import sys
#print >> sys.stderr, "ciao"

class Member(models.Model):
	username	= models.CharField(max_length=100)
	email		= models.EmailField()
	first_name	= models.CharField(max_length=200)
	last_name	= models.CharField(max_length=200)
	photo		= models.ImageField(upload_to='img/photo/')
	order		= models.PositiveSmallIntegerField(default=1)

	def __unicode__(self):
		return self.first_name + ' ' + self.last_name


class Membership(models.Model):
	start_date	= models.DateField(auto_now_add=True)
	end_date	= models.DateField()
	member		= models.ForeignKey(Member)
	
	def __unicode__(self):
		return self.member.username + ': '+ self.start_date.isoformat() + ' '+ self.end_date.isoformat()

#class Person(models.Model):
#	name	= models.CharField(max_length=100)
#	surname	= models.CharField(max_length=100)
#	photo		= models.ImageField(upload_to='images/photo/')
#	email	= models.EmailField(blank=True)
#	description = models.TextField(blank=True)


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