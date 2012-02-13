# -*- coding: utf-8 -*-
import datetime
from django.core.mail import EmailMultiAlternatives, mail_managers
from django.template.loader import get_template
from django.template import Context
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site


from op_associazione import settings

def send_mail(subject, txt_content, from_address, to_addresses, html_content=None):
    """send a multipart email according to arguments passed"""
    if not isinstance(to_addresses, (list, tuple)):
        to_addresses = [to_addresses]
    msg = EmailMultiAlternatives(subject, txt_content, from_address, to_addresses)
    if html_content is not None:
        msg.attach_alternative(html_content, "text/html")
    msg.send()


def send_checksubscriptions_report(expiring, expired):
    d = Context({ 'current_site': Site.objects.get(id=settings.SITE_ID),
                  'expiring': expiring, 'expired': expired, 'expiring_date': datetime.date.today() + datetime.timedelta(days=15) })

    # send notification to managers
    plaintext = get_template('email/checksubscriptions_report.txt')
    mail_managers('[openpolis] report controllo iscrizioni', plaintext.render(d))
    

def send_expiring_warning_email(membership):
    d = Context({ 'current_site': Site.objects.get(id=settings.SITE_ID),
                  'associate': membership.associate,
                  'expire_at': membership.expire_at.strftime("%d/%m/%Y"),
                  'renewal_url': reverse('subscribe-renewal', args=[membership.associate.hash_key]) })
    plaintext = get_template('email/expiring_warning_email.txt')
    htmly     = get_template('email/expiring_warning_email.html')
    
    send_mail(
        '[openpolis] Tua iscrizione in scadenza il %s' % (membership.expire_at.strftime("%d/%m/%Y")),
        plaintext.render(d),
        settings.SERVER_EMAIL,
        membership.associate.email,
        html_content=htmly.render(d)
    )

def send_expired_email(membership):
    d = Context({ 'current_site': Site.objects.get(id=settings.SITE_ID),
                  'associate': membership.associate,
                  'renewal_url': reverse('subscribe-renewal', args=[membership.associate.hash_key]) })
    plaintext = get_template('email/expired_email.txt')
    htmly     = get_template('email/expired_email.html')

    send_mail(
        '[openpolis] Tua iscrizione scaduta!',
        plaintext.render(d),
        settings.SERVER_EMAIL,
        membership.associate.email,
        html_content=htmly.render(d)
    )
    
def send_renewal_verification_email(associate):
    d = Context({ 'current_site': Site.objects.get(id=settings.SITE_ID),
                  'associate': associate,
                  'renewal_url': reverse('subscribe-renewal', args=[associate.hash_key]) })
    plaintext = get_template('email/renewal_verification_email.txt')
    htmly     = get_template('email/renewal_verification_email.html')
    
    send_mail(
        '[openpolis] Resta qui', 
        plaintext.render(d), 
        settings.SERVER_EMAIL, 
        associate.email,
        html_content=htmly.render(d)
    )

def subscription_received(membership, request_type):
    d = Context({ 'current_site': Site.objects.get(id=settings.SITE_ID),
                  'membership': membership, 'request_type': request_type })

    # send mail to requiring associate
    plaintext = get_template('email/your_subscription_received.txt')
    htmly     = get_template('email/your_subscription_received.html')
    
    if  request_type == 'renew':
        subject = '[openpolis] Ancora insieme'
    else:
        subject = '[openpolis] Benvenuto!'

    send_mail(
        subject, 
        plaintext.render(d), 
        settings.SERVER_EMAIL, 
        membership.associate.email,
        html_content=htmly.render(d)
    )
    
    # send notification to managers
    plaintext = get_template('email/new_subscription_received.txt')
    mail_managers('[openpolis] nuova iscrizione ricevuta', plaintext.render(d))
    
    
