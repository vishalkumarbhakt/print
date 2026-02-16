from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.files.storage import default_storage
from django.conf import settings
import os
import qrcode
from io import BytesIO
import json

from .models import PrintHistory
from .forms import PrintFileForm
from .printer_utils import PrinterManager


def home(request):
    """Home page view"""
    form = PrintFileForm()
    recent_prints = PrintHistory.objects.all()[:10]
    
    context = {
        'form': form,
        'recent_prints': recent_prints,
    }
    return render(request, 'printer/home.html', context)


def printer_status(request):
    """API endpoint to get printer status"""
    status = PrinterManager.get_printer_status()
    return JsonResponse(status)


def print_queue(request):
    """API endpoint to get print queue"""
    queue = PrinterManager.get_print_queue()
    return JsonResponse({'queue': queue})


def test_print(request):
    """API endpoint to print a test page"""
    success, message = PrinterManager.print_test_page()
    
    # Log to print history
    PrintHistory.objects.create(
        filename='Test Page',
        status='completed' if success else 'failed',
        error_message=None if success else message,
        ip_address=get_client_ip(request)
    )
    
    return JsonResponse({
        'success': success,
        'message': message
    })


@require_http_methods(["GET", "POST"])
def upload_and_print(request):
    """Handle file upload and printing"""
    if request.method == 'POST':
        form = PrintFileForm(request.POST, request.FILES)
        
        if form.is_valid():
            uploaded_file = form.cleaned_data['file']
            copies = form.cleaned_data['copies']
            
            # Save the file
            file_path = default_storage.save(
                f'print_files/{uploaded_file.name}',
                uploaded_file
            )
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)
            
            # Create print history record
            print_record = PrintHistory.objects.create(
                filename=uploaded_file.name,
                file_path=file_path,
                file_size=uploaded_file.size,
                status='pending',
                copies=copies,
                ip_address=get_client_ip(request)
            )
            
            # Try to print the file
            success, message = PrinterManager.print_file(full_path, copies)
            
            # Update print record
            print_record.status = 'completed' if success else 'failed'
            print_record.error_message = None if success else message
            print_record.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': success,
                    'message': message,
                    'filename': uploaded_file.name
                })
            else:
                return redirect('home')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Form validation failed',
                    'errors': form.errors
                }, status=400)
    
    return redirect('home')


def generate_qr(request):
    """Generate QR code for the print server URL"""
    # Get the host from request
    host = request.get_host()
    url = f"http://{host}/"
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save to BytesIO
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return HttpResponse(buffer.getvalue(), content_type='image/png')


def print_history_view(request):
    """View print history"""
    history = PrintHistory.objects.all()[:50]
    
    context = {
        'history': history,
    }
    return render(request, 'printer/history.html', context)


def print_history_json(request):
    """API endpoint to get print history as JSON"""
    history = PrintHistory.objects.all()[:50]
    
    data = []
    for record in history:
        data.append({
            'id': record.id,
            'timestamp': record.timestamp.isoformat(),
            'filename': record.filename,
            'status': record.status,
            'copies': record.copies,
            'file_size': record.file_size,
            'error_message': record.error_message,
        })
    
    return JsonResponse({'history': data})


def get_client_ip(request):
    """Get the client IP address from the request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

