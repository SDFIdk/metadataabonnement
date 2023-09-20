import csv
from django.core.management.base import BaseCommand
from metaSubscribe.models import Dataset

class Command(BaseCommand):
    help = "Import datasets from CSV file"

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        with open(csv_file_path, 'r', encoding='ISO-8859-1') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                Dataset.objects.create(
                    OBJECTID=row['OBJECTID'],
                    ID_LOKALID=row['ID_LOKALID'],
                    TITEL=row['TITEL']
                )
