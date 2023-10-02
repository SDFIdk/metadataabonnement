import csv
from django.core.management.base import BaseCommand
from metaSubscribe.models import Dataset

class Command(BaseCommand):
    help = 'Import data from a CSV file into the Dataset model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='/home/niksk/dockdockgo/compose_kursus/mysite/DATASETS.csv')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Dataset.objects.create(
                    OBJECTID=row['OBJECTID'],
                    ID_LOKALID=row['ID_LOKALID'],
                    TITEL=row['TITEL'],
                )
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
