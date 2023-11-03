from celery import shared_task
import django
from django.core.management import call_command
from django.utils import timezone
from main.helpers.mega import MegaFileUploader
from backup.models import DatabaseBackup
from datetime import datetime, timedelta


@shared_task(name="weekly_database_export")
def weekly_database_export():
    # Get today's date to use in the filename
    today = timezone.now()
    today_str = today.strftime("%Y_%m_%d")

    # Assuming `created_at` is a DateTimeField
    three_days_ago_start = datetime.combine(today.date() - timedelta(days=3), datetime.min.time())
    three_days_ago_start = timezone.make_aware(three_days_ago_start)  # if using timezone-aware datetimes
    
    # Check DB backup 
    db_backup_count = DatabaseBackup.objects.filter(created_at__gte=three_days_ago_start).count()
    if db_backup_count > 0 :
        print("Data Backup Already Done !!")
    else :
        json_db_path = f"db/database_backup_{today_str}.json"

        # Initialize Django.
        django.setup()

        # Perform the dumpdata command, excluding the specified models, and write to a file.
        with open(json_db_path, 'w', encoding='utf-8') as output_file:
            call_command(
                'dumpdata',
                exclude=['auth.permission', 'contenttypes'],
                stdout=output_file,
            )

        # Update Database in Mega.nz
        file_upload_link = MegaFileUploader().upload_file(json_db_path, "Database Backup")

        # Create Database Backup Entry
        DatabaseBackup.objects.create(**{"url": file_upload_link})

        print("Database Export Done Successfully !!")
