from optparse import make_option
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count

from op_associazione.models import Associate, Membership
from op_associazione import notifications

class Command(BaseCommand):
    help = 'Export memberships in csv format, optionally payed within a given year'

    option_list = BaseCommand.option_list + (
        make_option('--year',
            action='store',
            dest='year',
            default=None,
            help='List memberships payed in this fiscal year'),
    )

    def handle(self, *args, **options):
        """
        Extracts memberships.
        Send a report to site managers.
        Send a notification to expiring memberships related associates.
        
        De-activation must be manually performed by administrators.
        """

        memberships = Membership.objects.filter(payed_at__isnull=False)
        if options['year'] is not None:
            memberships = memberships.filter(payed_at__year=options['year'])
            
        self.stdout.write('Associato,Data pagamento,Quota\n')
        for m in memberships:
            self.stdout.write('%s,%s,%s\n' % 
                              (m.associate, m.payed_at.strftime('%d/%m/%Y'), m.fee,))
            