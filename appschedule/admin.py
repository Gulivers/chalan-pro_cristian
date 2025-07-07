from django.contrib import admin
from .models import Event, EventDraft, AbsenceReason


class BaseCrewTitleAdmin(admin.ModelAdmin):
    def crew_title(self, obj):
        if hasattr(obj, 'crew') and obj.crew:
            crew_name = obj.crew.name
            category = obj.crew.category.name if obj.crew.category else "No category"
            return f"{crew_name} ({category})"
        return "No crew assigned"

    crew_title.short_description = 'Crew'


@admin.register(Event)
class EventAdmin(BaseCrewTitleAdmin):
    list_display = ['title', 'date', 'end_dt', 'crew_title', 'builder', 'job', 'house_model', 'deleted']
    search_fields = ['title']
    list_filter = ['deleted', 'crew__category']


@admin.register(EventDraft)
class EventAdmin(BaseCrewTitleAdmin):
    list_display = ['title', 'date', 'end_dt', 'crew_title', 'builder', 'job', 'house_model']
    search_fields = ['title']
    list_filter = ['crew__category']

@admin.register(AbsenceReason)
class AbsenceReasonAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'is_active']
    search_fields = ['name', 'description']
    list_filter = ['is_active']