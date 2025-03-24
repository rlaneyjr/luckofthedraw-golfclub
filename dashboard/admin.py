from django.db.models import JSONField
from django.contrib import admin
from django.forms import widgets
from django_json_widget.widgets import JSONEditorWidget
from .models import *

# Customise the Admin title and header.
admin.site.site_title = "Luck of the Draw Golf Club"
admin.site.site_header = "Luck of the Draw Golf Club Admin"

# Register your models here.
admin.site.register(GolfCourse)
admin.site.register(Hole)
admin.site.register(Tee)
admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Group)
admin.site.register(PlayerMembership)
admin.site.register(HoleScore)
admin.site.register(TeeTime)

@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {'widget': JSONEditorWidget}
    }
