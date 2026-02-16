from django.db import models
from django.utils import timezone


class PrintHistory(models.Model):
    """Model to store print job history"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('printing', 'Printing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    timestamp = models.DateTimeField(default=timezone.now)
    filename = models.CharField(max_length=255)
    file_path = models.FileField(upload_to='print_files/', blank=True, null=True)
    file_size = models.IntegerField(help_text='File size in bytes', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    printer_name = models.CharField(max_length=255, default='HP LaserJet Pro 4004d')
    copies = models.IntegerField(default=1)
    error_message = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Print History'
        verbose_name_plural = 'Print Histories'
    
    def __str__(self):
        return f"{self.filename} - {self.timestamp} - {self.status}"

