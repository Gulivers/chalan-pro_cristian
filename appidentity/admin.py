from django.contrib import admin
from .models import Identity

@admin.register(Identity)
class IdentityAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'name', 'last_update')
    search_fields = ('name',)
    list_filter = ('last_update',)