from django.contrib import admin
from .models import Video
from django.http import HttpRequest
from django.utils.html import format_html



class VideoAdmin(admin.ModelAdmin):
    # set properties to display on list page
    list_display = (
        "title",
        "type",
        "year",
        "imdb_id",
        'get_imdb_link',
    )

    # handle list filtering
    search_fields = [
        "imdb_id",
        "title",
    ]
    list_filter = (
        "type",
    )
    
    # alter change view
    fields = (
        "imdb_id",
        "title",
        "type",
        "year",
    )

    # remove video creation option
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False

    # show imdb link
    def get_imdb_link(self, obj: Video) -> str:
        link = obj.generate_imdb_link()
        return format_html(f"<a target='_blank' href='{link}'>{link}</a>")
    get_imdb_link.short_description = "Link"


# register admin models
admin.site.register(Video, VideoAdmin)