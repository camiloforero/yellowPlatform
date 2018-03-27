from django.core.management.base import BaseCommand, CommandError
from yellowTools import scripts

class Command(BaseCommand):
    help = 'Loads all LC members from a period of time'

    def add_arguments(self, parser):
        #Positional arguments
        parser.add_argument('mc_id', nargs='+', type=int, help='EXPA ID del MC a cargar')

    def handle(self, *args, **options):
        #loadingScripts.loadWorldPerformance()
        for mc_id in options['mc_id']:
            scripts.load_country_EBs(mc_id)

