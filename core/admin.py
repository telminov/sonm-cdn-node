from django.contrib import admin

from core.models import CMSLog


class CMSLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'message', 'dc')
    list_filter = ('dc', )
    search_fields = ('action', 'message')


admin.site.register(CMSLog, CMSLogAdmin)