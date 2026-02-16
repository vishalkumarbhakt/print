"""
Printer utility functions for HP LaserJet Pro 4004d

This module handles all printer-related operations including:
- Printer status checking
- Print queue management
- Document printing (PDF, images, text files)
- PowerShell integration for advanced printer control
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

# Windows-specific imports (will be available on Windows only)
try:
    import win32print
    import win32api
    WINDOWS_AVAILABLE = True
except ImportError:
    WINDOWS_AVAILABLE = False
    # Mock functions for development on non-Windows systems
    class MockWin32Print:
        PRINTER_STATUS_READY = 0
        PRINTER_STATUS_PAUSED = 1
        PRINTER_STATUS_ERROR = 2
        PRINTER_STATUS_OFFLINE = 512
        
        @staticmethod
        def EnumPrinters(flags, name, level):
            return [
                (0, 0, 'HP LaserJet Pro 4004d', '', '', '')
            ]
        
        @staticmethod
        def GetDefaultPrinter():
            return 'HP LaserJet Pro 4004d'
        
        @staticmethod
        def OpenPrinter(printer_name):
            return 1
        
        @staticmethod
        def GetPrinter(handle, level):
            return {
                'Status': 0,
                'cJobs': 0,
                'pPrinterName': 'HP LaserJet Pro 4004d',
            }
        
        @staticmethod
        def ClosePrinter(handle):
            pass
        
        @staticmethod
        def EnumJobs(handle, first, count, level):
            return []
    
    win32print = MockWin32Print()
    
    class MockWin32Api:
        @staticmethod
        def ShellExecute(hwnd, operation, file, params, directory, show_cmd):
            print(f"Mock ShellExecute: {operation} {file}")
            return 42
    
    win32api = MockWin32Api()


class PrinterManager:
    """Manager class for printer operations"""
    
    PRINTER_NAME = "HP LaserJet Pro 4004d"
    
    @staticmethod
    def get_printer_status():
        """Get the current status of the printer"""
        try:
            if not WINDOWS_AVAILABLE:
                return {
                    'name': PrinterManager.PRINTER_NAME,
                    'status': 'online',
                    'status_code': 0,
                    'jobs_count': 0,
                    'is_default': True,
                    'message': 'Printer is ready (Mock mode - Windows not available)',
                }
            
            # Get printer handle
            handle = win32print.OpenPrinter(PrinterManager.PRINTER_NAME)
            printer_info = win32print.GetPrinter(handle, 2)
            
            # Parse status
            status_code = printer_info.get('Status', 0)
            status = 'online'
            message = 'Printer is ready'
            
            if status_code & win32print.PRINTER_STATUS_OFFLINE:
                status = 'offline'
                message = 'Printer is offline'
            elif status_code & win32print.PRINTER_STATUS_PAUSED:
                status = 'paused'
                message = 'Printer is paused'
            elif status_code & win32print.PRINTER_STATUS_ERROR:
                status = 'error'
                message = 'Printer has an error'
            
            jobs_count = printer_info.get('cJobs', 0)
            
            win32print.ClosePrinter(handle)
            
            return {
                'name': PrinterManager.PRINTER_NAME,
                'status': status,
                'status_code': status_code,
                'jobs_count': jobs_count,
                'is_default': win32print.GetDefaultPrinter() == PrinterManager.PRINTER_NAME,
                'message': message,
            }
        except Exception as e:
            return {
                'name': PrinterManager.PRINTER_NAME,
                'status': 'error',
                'status_code': -1,
                'jobs_count': 0,
                'is_default': False,
                'message': f'Error getting printer status: {str(e)}',
            }
    
    @staticmethod
    def get_print_queue():
        """Get the current print queue"""
        try:
            if not WINDOWS_AVAILABLE:
                return []
            
            handle = win32print.OpenPrinter(PrinterManager.PRINTER_NAME)
            jobs = win32print.EnumJobs(handle, 0, -1, 1)
            win32print.ClosePrinter(handle)
            
            queue = []
            for job in jobs:
                queue.append({
                    'job_id': job.get('JobId', 0),
                    'document': job.get('pDocument', 'Unknown'),
                    'status': job.get('Status', 0),
                    'pages': job.get('TotalPages', 0),
                    'submitted': job.get('Submitted', None),
                })
            
            return queue
        except Exception as e:
            print(f"Error getting print queue: {e}")
            return []
    
    @staticmethod
    def print_file(file_path, copies=1):
        """Print a file to the printer"""
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            if not WINDOWS_AVAILABLE:
                print(f"Mock print: {file_path} with {copies} copies")
                return True, "File sent to printer (Mock mode)"
            
            # Use ShellExecute to print the file
            # This will use the default application associated with the file type
            win32api.ShellExecute(
                0,
                "print",
                str(file_path),
                f'/d:"{PrinterManager.PRINTER_NAME}"',
                ".",
                0
            )
            
            return True, f"File sent to printer: {file_path.name}"
        except Exception as e:
            return False, f"Error printing file: {str(e)}"
    
    @staticmethod
    def print_test_page():
        """Print a test page using PowerShell"""
        try:
            if not WINDOWS_AVAILABLE or sys.platform != 'win32':
                print("Mock test page printed")
                return True, "Test page sent to printer (Mock mode)"
            
            # PowerShell command to print test page
            ps_command = f'''
            $printer = Get-Printer -Name "{PrinterManager.PRINTER_NAME}"
            $printer | Start-PrinterTest
            '''
            
            result = subprocess.run(
                ['powershell', '-Command', ps_command],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return True, "Test page sent to printer"
            else:
                return False, f"Error printing test page: {result.stderr}"
        except Exception as e:
            return False, f"Error printing test page: {str(e)}"
    
    @staticmethod
    def get_available_printers():
        """Get list of available printers"""
        try:
            if not WINDOWS_AVAILABLE:
                return ['HP LaserJet Pro 4004d (Mock)']
            
            printers = []
            for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS):
                printers.append(printer[2])
            
            return printers
        except Exception as e:
            print(f"Error getting printers: {e}")
            return []
