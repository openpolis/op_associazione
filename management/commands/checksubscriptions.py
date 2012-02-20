from optparse import make_option
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count

from op_associazione.models import Associate, Membership
from op_associazione import notifications

class Command(BaseCommand):
    help = 'Check memberhips for expiration and optionally notify consequently (send reminder to expiring, send report to site managers for both expiring and expired)'

    option_list = BaseCommand.option_list + (
        make_option('--send',
            action='store_true',
            dest='send',
            default=False,
            help='Send notifications to site managers and mail reminders to expiring memberships\' owners'),
    )

    def handle(self, *args, **options):
        """
        Extracts expiring (in N days) and expired memberships.
        Send a report to site managers.
        Send a notification to expiring memberships related associates.
        
        De-activation must be manually performed by administrators.
        """
        
        expiring = []
        expired = []
        
        # extracts associates having at least one membership
        associates = Associate.objects.annotate(n_memberships=Count('membership')).filter(n_memberships__gt=0)
        for associate in associates:
            # filter active memberships
            active_memberships = associate.memberships.order_by('-payed_at').filter(is_active=True)
            if len(active_memberships):
                # get last payed membership
                last_membership = active_memberships[0]
                # check if expire_at was filled, else fill it now (1 year )
                if last_membership.expire_at is None:
                    last_membership.expire_at = last_membership.payed_at + datetime.timedelta(days=365)
                    last_membership.save()
                    
                # check if membership is going to expire in 15 days
                if last_membership.expire_at == datetime.date.today() + datetime.timedelta(days=15):
                    # append to axpiring array, to send summary to managers
                    expiring.append(last_membership)
                    if options['send']:
                        # send mail to associate
                        notifications.send_expiring_warning_email(last_membership)

                    # log 
                    self.stdout.write('Associate: %s - payed_at: %s, expire_at: %s - Expiring!\n' % 
                                      (associate, last_membership.payed_at, last_membership.expire_at))
                    
                # check if membership is expired
                if last_membership.expire_at < datetime.date.today():
                    # append to expired array, to send summary to managers
                    expired.append(last_membership)
                        
                    self.stdout.write('Associate: %s - payed_at: %s, expire_at: %s - EXPIRED!\n' % 
                                      (associate, last_membership.payed_at, last_membership.expire_at))
                    
        if options['send']:
            notifications.send_checksubscriptions_report(expiring, expired)