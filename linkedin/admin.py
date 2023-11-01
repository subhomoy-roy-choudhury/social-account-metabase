from django.contrib import admin
from django.utils.html import format_html
from linkedin.models import LinkedinPost


# Reference Link :- https://testdriven.io/blog/customize-django-admin/
# Register your models here.
class CustomLinkedinPostAdmin(admin.ModelAdmin):
    model = LinkedinPost
    list_display = (
        "id",
        "linkedin_post_id",
        "is_send",
        "created_at",
        "updated_at",
        "linkedin_post_link",
    )
    list_filter = (
        "is_send",
        "created_at",
        "updated_at",
    )
    search_fields = ("linkedin_post_id",)
    ordering = ("created_at",)

    def linkedin_post_link(self, obj):
        LINEKDIN_POST_URL_FORMAT = (
            "https://www.linkedin.com/feed/update/urn:li:share:{linkedin_post_id}/"
        )
        return format_html(
            '<a class="button" target=”_blank” href="{}">Linkedin Post</a>&nbsp;',
            LINEKDIN_POST_URL_FORMAT.format(
                **{"linkedin_post_id": obj.linkedin_post_id}
            ),
        )


admin.site.register(LinkedinPost, CustomLinkedinPostAdmin)

admin.site.site_header = "Linkedin Post"
admin.site.site_title = "Backend Admin"
admin.site.index_title = "Oderna"
