from django.contrib import admin
from .models import PrintHistory


@admin.register(PrintHistory)
class PrintHistoryAdmin(admin.ModelAdmin):
    list_display = ['filename', 'timestamp', 'status', 'printer_name', 'copies', 'file_size']
    list_filter = ['status', 'timestamp', 'printer_name']
    search_fields = ['filename', 'printer_name', 'error_message']
    readonly_fields = ['timestamp']
    date_hierarchy = 'timestamp'

