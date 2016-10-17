from django.core.management.base import BaseCommand, CommandError
from yellowAnalytics import loadingScripts

class Command(BaseCommand):
    help = 'Reloads the world ranking'

    def handle(self, *args, **options):
        #loadingScripts.loadWorldPerformance()
        loadingScripts.refresh_rankings_v2()

