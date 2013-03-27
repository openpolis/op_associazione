from optparse import make_option
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count

from op_associazione.models import Associate, Membership
from op_associazione import notifications

class Command(BaseCommand):
    help = 'Export all subscribers, ever, paying or not'

    option_list = BaseCommand.option_list 

    def handle(self, *args, **options):
        """
        Extracts subscribers in CSV format
        """

        subscribers = Associate.objects.all()
            
        self.stdout.write('nome;cognome;email;location\n')
        for s in subscribers:
            self.stdout.write('%s;%s;%s;%s\n' % 
                              (s.first_name, s.last_name, s.email, s.location,))
            