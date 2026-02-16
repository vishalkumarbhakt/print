# Django HP LaserJet Pro 4004d Print Server

## Project Overview
This is a Django application designed to serve as a printer server specifically for HP LaserJet Pro 4004d printer. It provides a web interface for users to manage print jobs, monitor printer status, and access print history.

### Features
- 🖨️ **Print Documents**: Upload and print PDF, images, text files, and DOCX files
- 📊 **Printer Status**: Real-time monitoring of printer status and availability
- 📋 **Print Queue**: View and manage current print jobs in queue
- 🧪 **Test Printing**: Send test pages to verify printer functionality
- 📜 **Print History**: Track all print jobs with detailed history stored in database
- 📱 **QR Code Access**: Generate QR codes for easy mobile access to the print server
- 🔄 **Auto-refresh**: Automatic status updates every 5 seconds
- 💾 **Database Storage**: Print history stored in SQLite database (upgradable to PostgreSQL/MySQL)

### Technology Stack
- **Backend**: Django 4.0+
- **Database**: SQLite (default), supports PostgreSQL/MySQL
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla JS)
- **Printing**: Windows API (win32print, win32api)
- **QR Codes**: qrcode library with PIL
- **Image Processing**: Pillow

## Installation

### Prerequisites
- Python 3.8 or higher
- Windows OS (for printer functionality)
- HP LaserJet Pro 4004d printer installed and configured

### Setup Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vishalkumarbhakt/print.git
   cd print
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/Mac:
   source venv/bin/activate
   ```

3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Windows-specific dependencies** (Windows only):
   ```bash
   pip install pywin32
   ```

5. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser** (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   - Open your web browser and navigate to: `http://localhost:8000`
   - Admin panel: `http://localhost:8000/admin`

## Usage

### Printing a Document
1. Navigate to the home page
2. Click "Choose File" and select a document (PDF, PNG, JPG, TXT, DOCX)
3. Select number of copies (1-10)
4. Click "Upload & Print"
5. The document will be uploaded and sent to the printer

### Checking Printer Status
- The printer status is displayed in the header and updates automatically every 5 seconds
- View detailed printer information in the "Printer Controls" section

### Viewing Print Queue
- Click "Refresh Queue" button to see current jobs in the print queue
- View job ID, document name, and number of pages

### Print Test Page
- Click "Print Test Page" button to send a test page to the printer
- Useful for verifying printer connectivity and functionality

### Viewing Print History
- Recent prints (last 10) are shown on the home page
- Click "View Full History" to see complete print history
- Access admin panel for advanced filtering and management

### QR Code Access
- A QR code is displayed on the home page
- Scan with a mobile device to quickly access the print server
- Useful for sharing access on a local network

## Configuration

### Settings
Edit `print_server/settings.py` to customize:

- **ALLOWED_HOSTS**: Add your server's IP or domain
- **DATABASES**: Configure PostgreSQL or MySQL for production
- **STATIC_ROOT**: Change static files location
- **MEDIA_ROOT**: Change uploaded files location
- **FILE_UPLOAD_MAX_MEMORY_SIZE**: Adjust max file size (default: 10MB)

### Printer Configuration
Edit `printer/printer_utils.py` to change:

- **PRINTER_NAME**: Change the default printer name (line 75)
- Add support for additional printers

## API Endpoints

The application provides several API endpoints:

- `GET /api/printer-status/` - Get current printer status
- `GET /api/print-queue/` - Get current print queue
- `GET /api/test-print/` - Send a test page to printer
- `POST /upload/` - Upload and print a file
- `GET /qr-code/` - Generate QR code for server URL
- `GET /api/history/` - Get print history as JSON

## Production Deployment

### Using Gunicorn (Linux)
```bash
pip install gunicorn
gunicorn print_server.wsgi:application --bind 0.0.0.0:8000
```

### Using Waitress (Windows)
```bash
pip install waitress
waitress-serve --port=8000 print_server.wsgi:application
```

### Important Production Settings
1. Set `DEBUG = False` in settings.py
2. Set a secure `SECRET_KEY`
3. Configure `ALLOWED_HOSTS` properly
4. Use a production database (PostgreSQL/MySQL)
5. Configure static file serving with a web server (nginx/Apache)
6. Set up HTTPS/SSL certificates

## Troubleshooting

### Printer Not Found
- Verify HP LaserJet Pro 4004d is installed and set as default printer
- Check printer name matches in `printer_utils.py`
- Ensure printer is powered on and connected

### Upload Fails
- Check file size (must be under 10MB)
- Verify file format is supported
- Ensure media directory has write permissions

### Windows API Errors
- Install pywin32: `pip install pywin32`
- Run as administrator if permission issues occur

### Development on Non-Windows Systems
- The application includes mock implementations for development on Linux/Mac
- Actual printing will only work on Windows with printer drivers installed

## Contributing
Contributions are welcome! Please fork the repository and create a pull request for any changes you wish to propose.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
For any inquiries, please contact [vishalkumarbhakt](mailto:vishalkumarbhakt@example.com).
