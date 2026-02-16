"""
URL configuration for printer app
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/printer-status/', views.printer_status, name='printer_status'),
    path('api/print-queue/', views.print_queue, name='print_queue'),
    path('api/test-print/', views.test_print, name='test_print'),
    path('upload/', views.upload_and_print, name='upload_and_print'),
    path('qr-code/', views.generate_qr, name='generate_qr'),
    path('history/', views.print_history_view, name='print_history'),
    path('api/history/', views.print_history_json, name='print_history_json'),
]
