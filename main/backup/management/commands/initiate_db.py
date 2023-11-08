from django.core.management.base import BaseCommand
from main.helpers.mega import MegaFileUploader
import django
from django.core.management import call_command
from django.core.management.base import CommandError


class Command(BaseCommand):
    help = "Import Data for Sqlite3 Dump"

    def add_arguments(self, parser):
        parser.add_argument(
            "-u",
            "--url",
            type=str,
            help="Enter the Mega DB Backup Link",
        )

    def backup_db(self, link):
        # Download backup json
        mega = MegaFileUploader()
        filename = "database_backup.json"
        folderpath = "db"
        mega.download_file(link, folderpath, filename)

        # Initialize Django.
        django.setup()

        # Backup Data
        try:
            call_command("loaddata", f"{folderpath}/{filename}")
        except CommandError as e:
            print(f"An error occurred: {e}")

    def handle(self, *args, **kwargs):
        mega_db_backup_link = kwargs["url"]
        self.backup_db(mega_db_backup_link)
        print("Database Backup Done Successfully !!")
