# -*- coding: utf-8 -*-
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from models import OrderedModel
from django.db import transaction

from op_associazione import forms
from op_associazione.models import Membership
from django.template import  RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from django.template.loader import get_template
def static_page(request, page_slug):
	return render_to_response('statics/'+ page_slug +'.html', {},context_instance=RequestContext(request))

def payment(request):
	if request.session.get('associate-name', False) == False :
		return HttpResponse("Non hai effettuato l'accesso")
	return render_to_response( 'subscribe/payment.html' , {
		'associate_name' : request.session.get('associate-name'),
		'associate_fee' : request.session.get('associate-fee')
	},context_instance=RequestContext(request))

def renewal(request):
	return render_to_response( 'subscribe/renewal.html' , {},context_instance=RequestContext(request))

def renewal_request(request):
	if request.method == 'POST':
		form = forms.RenewalForm(request.POST)
		if form.is_valid() :
			email = form.cleaned_data.get("email")
			associate = form.associate
			last_membership = associate.membership_set()
			membership = Membership()
			
	else : 
		form = forms.RenewalForm()
		associate = False
	return render_to_response( 'subscribe/renewal.html' , {
		'form': form,
		'associate' : associate,
	},context_instance=RequestContext(request))

def subscribe(request):
	return render_to_response( 'subscribe/main.html' , {},context_instance=RequestContext(request))

def check_expedition_address(provided, form):
	if provided :
		return form.is_valid()
	return True

def subscribe_module(request, member_type):

	associate_form = build_associate_form(request,member_type)
	membership_form = build_membership_form(request,member_type)
	exp_address_provided = request.POST.get('expedition_address_provided', False)
	if request.method == 'POST': # If the form has been submitted...
		legal_address_form = forms.AddressForm(request.POST)
		expedition_address_form = forms.AddressForm(data=request.POST,prefix='exp')
		
#		if exp_address_provided:
#			expedition_address_form = forms.AddressForm(data=request.POST,prefix='exp')
#		else :
#			expedition_address_form = legal_address_form
		
		if associate_form.is_valid() & membership_form.is_valid() & legal_address_form.is_valid() & check_expedition_address(exp_address_provided,expedition_address_form): # All validation rules pass
			
			associate = associate_form.save(commit=False)
			associate.legal_address = legal_address_form.save()
			if exp_address_provided:
				associate.expedition_address = expedition_address_form.save()
			else :
				associate.expedition_address = associate.legal_address
			associate.save()
			
			membership = membership_form.save(commit=False)
			membership.associate = associate;
			membership.save()
			
			request.session['associate-name'] = associate.first_name
			request.session['associate-fee'] = membership.fee

			return HttpResponseRedirect(reverse('subscribe-pay')) # Redirect after POST
	else :
		legal_address_form = forms.AddressForm()
		expedition_address_form = forms.AddressForm(prefix='exp')
		
	return render_to_response('subscribe/'+ member_type +'_form.html', {
		'associate_form' : associate_form,
		'membership_form' : membership_form,
		'legal_address_form' : legal_address_form,
		'expedition_address_form' : expedition_address_form,
		'expedition_address_provided' : exp_address_provided,
		'member_type' : member_type
	}, context_instance=RequestContext(request))

def build_membership_form(request, member_type):
	if request.method == 'POST' :
		form = forms.MembershipForm(data=request.POST)
	else :
		form = forms.MembershipForm()
	
	if member_type == 'cittadino' :
		form.fields['type_of_membership'].widget.choices = Membership.MEMBER_TYPE[1:4]
	else :
		form.fields['type_of_membership'].widget.choices = Membership.MEMBER_TYPE[1:3]
		
	return form

def build_associate_form(request, member_type):
	if request.method == 'POST' :
		if member_type == 'cittadino':
			form = forms.CitizenForm(data=request.POST)
		elif member_type == 'politico':
			form = forms.PoliticianForm(data=request.POST)
		elif member_type == 'organizzazione':
			form = forms.OrganizationForm(data=request.POST)
	else :
		if member_type == 'cittadino':
			form = forms.CitizenForm()
		elif member_type == 'politico':
			form = forms.PoliticianForm()
		elif member_type == 'organizzazione':
			form = forms.OrganizationForm()
	return form

@staff_member_required
@transaction.commit_on_success
def admin_move_ordered_model(request, direction, model_type_id, model_id):
    if direction == "up":
        OrderedModel.move_up(model_type_id, model_id)
    else:
        OrderedModel.move_down(model_type_id, model_id)
    
    ModelClass = ContentType.objects.get(id=model_type_id).model_class()
    
    app_label = ModelClass._meta.app_label
    model_name = ModelClass.__name__.lower()

    url = "/admin/%s/%s/" % (app_label, model_name)
    
    return HttpResponseRedirect(url)