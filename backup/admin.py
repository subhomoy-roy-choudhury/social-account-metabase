from django.contrib import admin
from backup.models import DatabaseBackup
from django.utils.html import format_html


# Register your models here.
class CustomDatabaseBackupAdmin(admin.ModelAdmin):
    model = DatabaseBackup
    list_display = (
        "id",
        "mega_db_backup_link",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "created_at",
        "updated_at",
    )
    search_fields = ("linkedin_post_id",)
    ordering = ("-created_at",)

    def mega_db_backup_link(self, obj):
        return format_html(
            f'<a class="button" target=”_blank” href="{obj.url}">Backup Link</a>&nbsp;',
        )


admin.site.register(DatabaseBackup, CustomDatabaseBackupAdmin)
