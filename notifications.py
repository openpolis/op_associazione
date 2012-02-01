# -*- coding: utf-8 -*-
from django.core.mail import EmailMultiAlternatives, mail_managers
from django.template.loader import get_template
from django.template import Context
from django.core.urlresolvers import reverse

from op_associazione import settings

def send_mail(subject, txt_content, from_address, to_addresses, html_content=None):
    """send a multipart email according to arguments passed"""
    if not isinstance(to_addresses, (list, tuple)):
        to_addresses = [to_addresses]
    msg = EmailMultiAlternatives(subject, txt_content, from_address, to_addresses)
    if html_content is not None:
        msg.attach_alternative(html_content, "text/html")
    msg.send()

def send_renewal_email(associate):
    d = Context({ 'renewal_url': reverse('subscribe-renewal', args=[associate.hash_key]) })
    plaintext = get_template('email/renewal_email.txt')
    htmly     = get_template('email/renewal_email.html')
    
    send_mail(
        '[openpolis] Rinnova la tua iscrizione!', 
        plaintext.render(d), 
        settings.SERVER_EMAIL, 
        associate.email,
        html_content=htmly.render(d)
    )

def subscription_received(membership, request_type):
    d = Context({ 'membership': membership, 'request_type': request_type })

    # send mail to requiring associate
    plaintext = get_template('email/your_subscription_received.txt')
    htmly     = get_template('email/your_subscription_received.html')
    
    send_mail(
        '[openpolis] Benvenuto!', 
        plaintext.render(d), 
        settings.SERVER_EMAIL, 
        membership.associate.email,
        html_content=htmly.render(d)
    )
    
    # send notification to managers
    plaintext = get_template('email/new_subscription_received.txt')
    mail_managers('[openpolis] nuova iscrizione ricevuta', plaintext.render(d))