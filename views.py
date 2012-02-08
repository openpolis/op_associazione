# -*- coding: utf-8 -*-
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponseRedirect
from django.db import transaction
from django.template import  RequestContext
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse

from copy import deepcopy
import hashlib

from django.template.loader import get_template

from op_associazione.models import OrderedModel, Membership, Associate
from op_associazione import forms
from op_associazione import notifications


def static_page(request, page_slug):
    return render_to_response('statics/'+ page_slug +'.html', {'page_slug': page_slug},context_instance=RequestContext(request))

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
        return HttpResponseRedirect(reverse('subscribe-renewal-request')) # Problems! Redirect to mail form
    
    if not last_membership.is_active:
        return HttpResponseRedirect(reverse('subscribe-renewal-request')) # Problems! Redirect to mail form
    
    from datetime import timedelta
    next_expire = last_membership.expire_at + timedelta(days=365)
    
    form = build_membership_form(request, membership=last_membership)
    if request.method == 'POST':
        if form.is_valid():
            # Create new Membership..
            new_membership = form.save(commit=False)
            new_membership.associate = associate
            new_membership.save()
            
            notifications.subscription_received(new_membership, 'renew')
            
            request.session['associate-name'] = associate.first_name
            request.session['associate-fee'] = new_membership.fee
            request.session['associate-renewal'] = next_expire
            return HttpResponseRedirect(reverse('subscribe-pay')) # Redirect

    return render_to_response( 'subscribe/renewal.html' , {
        'form' : form,
        'associate' : associate,
        'last_membership' : last_membership,
        'next_expire' : next_expire,
    },context_instance=RequestContext(request))


def renewal_request(request):
    associate = False
    if request.method == 'POST':
        form = forms.RenewalRequestForm(request.POST)
        if form.is_valid() :         
            associate = form.associate   

            # Send mail to confirm
            notifications.send_renewal_email(associate)
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
    membership_form = build_membership_form(request,member_type=member_type)
    exp_address_provided = request.POST.get('exp_address_provided', False)
    if request.method == 'POST': # If the form has been submitted...

        if associate_form.is_valid() & membership_form.is_valid(): # All validation rules pass
            
            associate = associate_form.save(commit=False)
            # Check if Expedition Address is provided
            if not exp_address_provided:
                associate.exp_street = associate.street
                associate.exp_civic_nb = associate.civic_nb
                associate.exp_zip_code = associate.zip_code
                associate.exp_location = associate.location
                associate.exp_province = associate.province
                associate.exp_country = associate.country

            # Build the activation key for their account
            associate.hash_key = hashlib.sha1(associate.email).hexdigest()
            # Save it
            associate.save()

            membership = membership_form.save(commit=False)
            membership.associate = associate;
            membership.save()

            notifications.subscription_received(membership, 'first')

            request.session['associate-name'] = associate.first_name
            request.session['associate-fee'] = membership.fee

            return HttpResponseRedirect(reverse('subscribe-pay')) # Redirect after POST
        
    return render_to_response('subscribe/'+ member_type +'_form.html', {
        'associate_form' : associate_form,
        'membership_form' : membership_form,
        'member_type' : member_type
    }, context_instance=RequestContext(request))

def build_membership_form(request, membership=None, member_type=None):
    if request.method == 'POST' :
        form = forms.MembershipForm(data=request.POST)
    else :
        form = forms.MembershipForm(instance=membership)
    
    
    if member_type is not None:
        if member_type == 'cittadino':
            form.fields['type_of_membership'].widget.choices = Membership.MEMBER_TYPE[1:4]
        else:
            form.fields['type_of_membership'].widget.choices = Membership.MEMBER_TYPE[1:3]
        return form
        
        
    # test if membership is owned by a citizen or not
    if membership is not None:
        try:
            c = membership.associate.citizen
            form.fields['type_of_membership'].widget.choices = Membership.MEMBER_TYPE[1:4]
        except Exception, e:
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