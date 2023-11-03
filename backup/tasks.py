from celery import shared_task
import sqlite3
from django.apps import apps
from django.db import connections, transaction, connection
from django.utils import timezone
from main.helpers.mega import MegaFileUploader
from backup.models import DatabaseBackup
from datetime import datetime, timedelta


def get_sqlite_create_table_sql(model_class):
    fields = model_class._meta.fields
    field_sql = []

    # Use a database connection to get the correct db_type
    with connection.cursor() as cursor:
        for field in fields:
            # Get the column definition in SQLite's dialect
            db_type = field.db_type(connection=connection)
            # Ensure the db_type is not None
            if db_type is None:
                raise TypeError(
                    f"Cannot determine the db_type for field {field.name} in model {model_class.__name__}"
                )
            field_sql.append(f'"{field.column}" {db_type}')

        # Construct the complete CREATE TABLE statement
        table_sql = f'CREATE TABLE IF NOT EXISTS "{model_class._meta.db_table}" ({", ".join(field_sql)});'

    return table_sql


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
        # Define the SQLite database path with the current date
        sqlite_db_path = f"db/database_backup_{today_str}.db"

        # Establish a connection to the SQLite database
        sqlite_conn = sqlite3.connect(sqlite_db_path)
        sqlite_cursor = sqlite_conn.cursor()

        # Use the 'default' database connection for PostgreSQL
        django_pg_conn = connections["default"]

        # Get all models in the app
        models = apps.get_models()

        for model in models:
            # Only proceed with models that are not abstract and are managed by Django
            if model._meta.app_label != "auth" and not model._meta.auto_created:
                if not model._meta.abstract and model._meta.managed:
                    table_name = model._meta.db_table
                    columns = [field.column for field in model._meta.fields]
                    column_names = ", ".join(columns)
                    placeholders = ", ".join("?" for _ in columns)

                    # Create the table in SQLite
                    create_table_statement = get_sqlite_create_table_sql(model)
                    sqlite_cursor.execute(create_table_statement)

                    # Fetch data from PostgreSQL
                    with transaction.atomic(using="default"):
                        for obj in model.objects.all().iterator():
                            values = [
                                getattr(obj, field.attname) for field in model._meta.fields
                            ]

                            # Insert data into SQLite
                            sqlite_cursor.execute(
                                f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})",
                                values,
                            )

                    # Commit the changes to the SQLite database
                    sqlite_conn.commit()

        # Close the SQLite connection
        sqlite_cursor.close()
        sqlite_conn.close()

        # Update Database in Mega.nz
        # Upload a file
        file_upload_link = MegaFileUploader().upload_file(sqlite_db_path, "Database Backup")

        # Create Database Backup Entry
        DatabaseBackup.objects.create(**{"url": file_upload_link})

        print("Database Export Done Successfully !!")
