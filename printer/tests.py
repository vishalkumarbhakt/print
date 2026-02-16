from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import PrintHistory
import json


class PrinterViewTests(TestCase):
    """Test cases for printer views"""
    
    def setUp(self):
        self.client = Client()
    
    def test_home_page(self):
        """Test that home page loads successfully"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'HP LaserJet Pro 4004d')
    
    def test_printer_status_api(self):
        """Test printer status API endpoint"""
        response = self.client.get('/api/printer-status/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('name', data)
        self.assertIn('status', data)
        self.assertEqual(data['name'], 'HP LaserJet Pro 4004d')
    
    def test_print_queue_api(self):
        """Test print queue API endpoint"""
        response = self.client.get('/api/print-queue/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('queue', data)
        self.assertIsInstance(data['queue'], list)
    
    def test_history_api(self):
        """Test print history API endpoint"""
        response = self.client.get('/api/history/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('history', data)
        self.assertIsInstance(data['history'], list)
    
    def test_test_print_api(self):
        """Test print test page API"""
        response = self.client.get('/api/test-print/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('success', data)
        self.assertIn('message', data)
        
        # Verify print history was created
        history = PrintHistory.objects.filter(filename='Test Page')
        self.assertTrue(history.exists())
    
    def test_qr_code_generation(self):
        """Test QR code generation"""
        response = self.client.get('/qr-code/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'image/png')
    
    def test_file_upload(self):
        """Test file upload and print"""
        test_file = SimpleUploadedFile(
            "test.txt",
            b"Test document content",
            content_type="text/plain"
        )
        
        response = self.client.post(
            '/upload/',
            {
                'file': test_file,
                'copies': 1
            },
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('success', data)
        
        # Verify print history was created
        history = PrintHistory.objects.filter(filename='test.txt')
        self.assertTrue(history.exists())
    
    def test_print_history_page(self):
        """Test print history page loads"""
        response = self.client.get('/history/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Print History')


class PrintHistoryModelTests(TestCase):
    """Test cases for PrintHistory model"""
    
    def test_create_print_history(self):
        """Test creating a print history record"""
        record = PrintHistory.objects.create(
            filename='test.pdf',
            status='completed',
            copies=2
        )
        self.assertEqual(record.filename, 'test.pdf')
        self.assertEqual(record.status, 'completed')
        self.assertEqual(record.copies, 2)
        self.assertEqual(record.printer_name, 'HP LaserJet Pro 4004d')
    
    def test_print_history_ordering(self):
        """Test that print history is ordered by timestamp descending"""
        PrintHistory.objects.create(filename='first.pdf', status='completed')
        PrintHistory.objects.create(filename='second.pdf', status='completed')
        
        records = PrintHistory.objects.all()
        self.assertEqual(records[0].filename, 'second.pdf')
        self.assertEqual(records[1].filename, 'first.pdf')

