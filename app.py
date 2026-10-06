from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os
import json
import tempfile
from werkzeug.utils import secure_filename
from datetime import datetime
from io import BytesIO

app = Flask(__name__, static_folder='static', template_folder='static')
app.config['MAX_CONTENT_LENGTH'] = None  # No limit on Render

# Gofile API Configuration
API_KEY = "YOUR_GOFILE_API_KEY"
API_BASE = "https://api.gofile.io"

# Discord Webhook Configuration
DISCORD_WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"

class GofileUploader:
    def __init__(self):
        self.server = None
        self.account_info = None
        self.root_folder_id = None
        self.initialize()
    
    def initialize(self):
        """Initialize connection to Gofile"""
        self.get_server()
        self.get_account_info()
    
    def get_account_info(self):
        """Get account information"""
        try:
            headers = {'Authorization': f'Bearer {API_KEY}'}
            response = requests.get(f'{API_BASE}/accounts/getid', headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'ok':
                    self.account_info = data.get('data', {})
                    self.root_folder_id = self.account_info.get('rootFolder', None)
                    return True
        except Exception as e:
            print(f"Error getting account info: {e}")
        return False
    
    def get_server(self):
        """Get best available server"""
        try:
            response = requests.get(f'{API_BASE}/servers', timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'ok' and data['data']['servers']:
                    servers = data['data']['servers']
                    best_server = min(servers, key=lambda x: x.get('load', 100))
                    self.server = best_server['name']
                    return True
        except Exception as e:
            print(f"Error getting server: {e}")
        self.server = 'store1'
        return True
    
    def upload_file(self, file_data, file_name, folder_id=None):
        """Upload file to Gofile"""
        try:
            headers = {'Authorization': f'Bearer {API_KEY}'}
            
            files = {'file': (file_name, file_data)}
            data = {}
            if folder_id:
                data['folderId'] = folder_id
            elif self.root_folder_id:
                data['folderId'] = self.root_folder_id
            
            upload_url = f'https://{self.server}.gofile.io/contents/uploadfile'
            
            response = requests.post(
                upload_url,
                files=files,
                data=data,
                headers=headers,
                timeout=None
            )
            
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get('status') == 'ok':
                    download_link = self.extract_download_link(response_data)
                    return {
                        'success': True,
                        'link': download_link,
                        'data': response_data
                    }
                else:
                    return {
                        'success': False,
                        'error': response_data.get('status', 'Unknown error')
                    }
            else:
                return {
                    'success': False,
                    'error': f'Upload failed with status code: {response.status_code}'
                }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def extract_download_link(self, data):
        """Extract download link from response"""
        try:
            data_obj = data.get('data', {})
            
            if isinstance(data_obj, dict):
                if 'downloadPage' in data_obj:
                    return data_obj['downloadPage']
                elif 'file' in data_obj and isinstance(data_obj['file'], dict):
                    file_obj = data_obj['file']
                    if 'downloadPage' in file_obj:
                        return file_obj['downloadPage']
                    elif 'link' in file_obj:
                        return file_obj['link']
                elif 'link' in data_obj:
                    return data_obj['link']
                elif 'url' in data_obj:
                    return data_obj['url']
                elif 'fileId' in data_obj:
                    return f"https://gofile.io/d/{data_obj['fileId']}"
                elif 'contentId' in data_obj:
                    return f"https://gofile.io/d/{data_obj['contentId']}"
            elif isinstance(data_obj, str) and data_obj.startswith('http'):
                return data_obj
        except Exception as e:
            print(f"Error extracting link: {e}")
        return None

uploader = GofileUploader()

def get_client_ip():
    """Get client IP address"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr

def get_device_info():
    """Get device information from user agent"""
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    device_type = "Desktop"
    if 'Mobile' in user_agent:
        device_type = "Mobile"
    elif 'Tablet' in user_agent:
        device_type = "Tablet"
    
    browser = "Unknown"
    if 'Chrome' in user_agent:
        browser = "Chrome"
    elif 'Firefox' in user_agent:
        browser = "Firefox"
    elif 'Safari' in user_agent:
        browser = "Safari"
    elif 'Edge' in user_agent:
        browser = "Edge"
    elif 'Opera' in user_agent:
        browser = "Opera"
    
    os_name = "Unknown"
    if 'Windows' in user_agent:
        os_name = "Windows"
    elif 'Mac' in user_agent:
        os_name = "macOS"
    elif 'Linux' in user_agent:
        os_name = "Linux"
    elif 'Android' in user_agent:
        os_name = "Android"
    elif 'iOS' in user_agent or 'iPhone' in user_agent or 'iPad' in user_agent:
        os_name = "iOS"
    
    return {
        'device_type': device_type,
        'browser': browser,
        'os': os_name,
        'user_agent': user_agent
    }

def get_location_info(ip):
    """Get location info from IP"""
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}', timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                return {
                    'country': data.get('country', 'Unknown'),
                    'city': data.get('city', 'Unknown'),
                    'region': data.get('regionName', 'Unknown'),
                    'isp': data.get('isp', 'Unknown'),
                    'lat': data.get('lat', 'Unknown'),
                    'lon': data.get('lon', 'Unknown'),
                    'timezone': data.get('timezone', 'Unknown')
                }
    except:
        pass
    return None

def send_discord_webhook(title, description, color=0x00ff00, fields=None):
    """Send webhook to Discord"""
    try:
        embed = {
            "title": title,
            "description": description,
            "color": color,
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {
                "text": "File Uploader by @Hidden_Rhyhtm"
            }
        }
        
        if fields:
            embed["fields"] = fields
        
        payload = {
            "embeds": [embed]
        }
        
        response = requests.post(
            DISCORD_WEBHOOK_URL,
            json=payload,
            timeout=5
        )
        
        if response.status_code == 204:
            print("Webhook sent successfully")
        else:
            print(f"Webhook failed: {response.status_code}")
    except Exception as e:
        print(f"Error sending webhook: {e}")

@app.route('/')
def index():
    """Serve main page and log visitor info"""
    ip = get_client_ip()
    device_info = get_device_info()
    location = get_location_info(ip)
    
    fields = [
        {"name": "🌐 IP Address", "value": f"`{ip}`", "inline": True},
        {"name": "💻 Device", "value": f"`{device_info['device_type']}`", "inline": True},
        {"name": "🌍 Browser", "value": f"`{device_info['browser']}`", "inline": True},
        {"name": "🖥️ OS", "value": f"`{device_info['os']}`", "inline": True}
    ]
    
    if location:
        fields.extend([
            {"name": "📍 Location", "value": f"`{location['city']}, {location['country']}`", "inline": True},
            {"name": "🏢 ISP", "value": f"`{location['isp']}`", "inline": True},
            {"name": "🕐 Timezone", "value": f"`{location['timezone']}`", "inline": True}
        ])
    
    fields.append({"name": "🔍 User Agent", "value": f"`{device_info['user_agent'][:100]}`", "inline": False})
    
    send_discord_webhook(
        title="👤 New Visitor",
        description=f"Someone visited the uploader at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        color=0x3498db,
        fields=fields
    )
    
    return send_from_directory('static', 'index.html')

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/style.css')
def style():
    """Serve CSS"""
    return send_from_directory('static', 'style.css', mimetype='text/css')

@app.route('/api/account-info')
def account_info():
    """Get account information"""
    if uploader.account_info:
        return jsonify({
            'success': True,
            'account': uploader.account_info,
            'server': uploader.server
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Not connected to account'
        })

@app.route('/api/upload', methods=['POST'])
def upload():
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file provided'})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No file selected'})
    
    ip = get_client_ip()
    device_info = get_device_info()
    location = get_location_info(ip)
    
    folder_id = request.form.get('folderId', None)
    filename = secure_filename(file.filename)
    
    # Read file into memory
    file_data = file.read()
    
    try:
        result = uploader.upload_file(BytesIO(file_data), filename, folder_id)
        
        if result['success']:
            file_size = len(file_data)
            if file_size > 1024 * 1024:
                file_size_str = f"{file_size / (1024 * 1024):.2f} MB"
            else:
                file_size_str = f"{file_size / 1024:.2f} KB"
            
            fields = [
                {"name": "📁 File Name", "value": f"`{filename}`", "inline": True},
                {"name": "📏 File Size", "value": f"`{file_size_str}`", "inline": True},
                {"name": "🔗 Download Link", "value": f"`{result['link']}`", "inline": False},
                {"name": "🌐 IP Address", "value": f"`{ip}`", "inline": True},
                {"name": "💻 Device", "value": f"`{device_info['device_type']} - {device_info['os']}`", "inline": True}
            ]
            
            if location:
                fields.append({"name": "📍 Location", "value": f"`{location['city']}, {location['country']}`", "inline": True})
            
            send_discord_webhook(
                title="✅ File Uploaded",
                description=f"File uploaded successfully at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                color=0x00ff00,
                fields=fields
            )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))