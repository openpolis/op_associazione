# -*- coding: utf-8 -*-
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from models import OrderedModel
from django.db import transaction

from op_associazione import forms
from op_associazione.models import Membership, Associate
from django.template import  RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from copy import deepcopy
import hashlib

from django.template.loader import get_template
def static_page(request, page_slug):
    return render_to_response('statics/'+ page_slug +'.html', {},context_instance=RequestContext(request))

def payment(request):
    if request.session.get('associate-name', False) == False :
        return HttpResponse("Non siamo riusciti ad identificarti")
    return render_to_response( 'subscribe/payment.html' , {
        'associate_name' : request.session.get('associate-name'),
        'associate_fee' : request.session.get('associate-fee'),
        'renewal' : request.session.get('associate-renewal')
    },context_instance=RequestContext(request))


def renewal(request, user_hash):
    associate = Associate.objects.get(hash_key=user_hash)
    try:
        last_membership = associate.membership_set.latest('expire_at')
    except Membership.DoesNotExist:
        return HttpResponseRedirect(reverse('subscribe-renewal-request')) # Redirect
    
    if not last_membership.is_active:
        return HttpResponseRedirect(reverse('subscribe-renewal-request')) # Redirect
    
    from datetime import timedelta
    next_expire = last_membership.expire_at + timedelta(days=365)
    
    if request.method == 'POST':
        form = forms.MembershipForm(request.POST)
        if form.is_valid():
            # Create new Membership..
            new_membership = form.save(commit=False)
            new_membership.associate = associate
            new_membership.save()
            request.session['associate-name'] = associate.first_name
            request.session['associate-fee'] = new_membership.fee
            request.session['associate-renewal'] = next_expire
            return HttpResponseRedirect(reverse('subscribe-pay')) # Redirect
    else:
        form = forms.MembershipForm(instance=last_membership)

    return render_to_response( 'subscribe/renewal.html' , {
        'form' : form,
        'associate' : associate,
        'last_membership' : last_membership,
        'next_expire' : next_expire,
    },context_instance=RequestContext(request))

def send_renewal_email(associate):
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import get_template
    from django.template import Context
    from op_associazione import settings
    
    plaintext = get_template('email/renewal_email.txt')
    htmly     = get_template('email/renewal_email.html')

    d = Context({ 'renewal_url': reverse('subscribe-renewal', args=[associate.hash_key]) })

    subject, from_email, to = 'Rinnova l\'associazione ad Openpolis', 'no-reply@openpolis.it', associate.email
    text_content = plaintext.render(d)
    html_content = htmly.render(d)
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

def renewal_request(request):
    associate = False
    if request.method == 'POST':
        form = forms.RenewalRequestForm(request.POST)
        if form.is_valid() :         
            associate = form.associate   
            # Send mail to confirm
            send_renewal_email(associate)
    else : 
        form = forms.RenewalRequestForm()
	
    return render_to_response( 'subscribe/renewal_request.html' , {
        'form': form,
        'associate': associate
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

        if associate_form.is_valid() & membership_form.is_valid() & legal_address_form.is_valid() & check_expedition_address(exp_address_provided,expedition_address_form): # All validation rules pass
			
            associate = associate_form.save(commit=False)
            associate.legal_address = legal_address_form.save()
            # Check if Expedition Address is provided
            if exp_address_provided:
                associate.expedition_address = expedition_address_form.save()
            else :
                old_obj = deepcopy(associate.legal_address)
                old_obj.id = None
                old_obj.save()
                associate.expedition_address = old_obj                

            # Build the activation key for their account
            
            associate.hash_key = hashlib.sha1(associate.email).hexdigest()
            # Save it
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