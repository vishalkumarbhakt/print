"""
Django forms for the printer app
"""

from django import forms
from .models import PrintHistory


class PrintFileForm(forms.Form):
    """Form for uploading and printing files"""
    
    file = forms.FileField(
        label='Select file to print',
        help_text='Supported formats: PDF, PNG, JPG, TXT, DOCX',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.png,.jpg,.jpeg,.txt,.docx'
        })
    )
    
    copies = forms.IntegerField(
        label='Number of copies',
        initial=1,
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '10'
        })
    )
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        
        if file:
            # Check file size (10MB limit)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError('File size must be less than 10MB')
            
            # Check file extension
            allowed_extensions = ['.pdf', '.png', '.jpg', '.jpeg', '.txt', '.docx']
            ext = file.name.lower().split('.')[-1]
            if f'.{ext}' not in allowed_extensions:
                raise forms.ValidationError(
                    f'File type not supported. Allowed types: {", ".join(allowed_extensions)}'
                )
        
        return file
