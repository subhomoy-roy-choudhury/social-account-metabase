from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Import Data for DBSqlite Dump'

    def add_arguments(self, parser):
        # parser.add_argument('model_name', type=str, help='Name of the Elastic Search model')
        # parser.add_argument('-a', '--app_name', type=str, help='Name of the Django APP', )
        pass

    def handle(self, *args, **kwargs):
        # model_name = kwargs['model_name']
        # app_name = kwargs['app_name']

        pass