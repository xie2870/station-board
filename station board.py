import http.server
import socketserver
import threading
import time
import json
import socket
import urllib.parse
from datetime import datetime

# Configuration
DATA_FILE = "schedule.txt"
PORT = 8080

# HTML Template - Main Page (English)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="10">
    <title>Metro Digital Sign - {station_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
            background: #0a0e1a;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}

        .display-board {{
            max-width: 1200px;
            width: 100%;
            background: linear-gradient(145deg, #101624 0%, #0c1020 100%);
            border-radius: 40px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.05);
            border: 1px solid #2a3450;
        }}

        .station-header {{
            background: linear-gradient(135deg, #1a6e3f 0%, #0e4f2d 100%);
            border-radius: 24px;
            padding: 25px 35px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 8px 20px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.2);
            border-bottom: 3px solid #2ed15e;
            position: relative;
        }}

        .nav-buttons {{
            position: absolute;
            right: 30px;
            top: 50%;
            transform: translateY(-50%);
            display: flex;
            gap: 15px;
        }}

        .nav-btn {{
            background: rgba(0,0,0,0.5);
            border: 1px solid #2ed15e;
            color: #2ed15e;
            font-size: 28px;
            font-weight: bold;
            width: 50px;
            height: 50px;
            border-radius: 25px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.3s;
            font-family: monospace;
        }}

        .nav-btn:hover {{
            background: #2ed15e;
            color: #0a0e1a;
            transform: scale(1.05);
        }}

        .settings-btn {{
            position: absolute;
            left: 30px;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(0,0,0,0.5);
            border: 1px solid #7ee0ff;
            color: #7ee0ff;
            font-size: 20px;
            padding: 8px 16px;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
        }}

        .settings-btn:hover {{
            background: #7ee0ff;
            color: #0a0e1a;
        }}

        .station-name {{
            font-size: 48px;
            font-weight: bold;
            letter-spacing: 4px;
            color: #ffffff;
            text-shadow: 0 2px 5px rgba(0,0,0,0.3);
        }}

        .station-sub {{
            font-size: 18px;
            color: #c8e6d9;
            margin-top: 10px;
            letter-spacing: 2px;
        }}

        .station-indicator {{
            position: absolute;
            left: 120px;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(0,0,0,0.5);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            color: #7ee0ff;
        }}

        .info-bar {{
            display: flex;
            justify-content: space-between;
            background: rgba(0,0,0,0.4);
            border-radius: 16px;
            padding: 12px 20px;
            margin-bottom: 25px;
            font-size: 18px;
            color: #bbd4f0;
        }}

        .update-time {{
            font-family: monospace;
            font-size: 20px;
            color: #7ee0ff;
        }}

        .keyboard-hint {{
            font-size: 14px;
            color: #6a7c9e;
            margin-top: 20px;
            text-align: center;
            padding: 10px;
            border-top: 1px solid #1e2840;
        }}

        .keyboard-hint span {{
            display: inline-block;
            background: #1e2840;
            padding: 4px 12px;
            border-radius: 8px;
            margin: 0 5px;
            font-family: monospace;
            font-weight: bold;
        }}

        .trains-table {{
            width: 100%;
            border-collapse: collapse;
        }}

        .trains-table th {{
            text-align: left;
            padding: 16px 20px;
            background: rgba(30, 40, 60, 0.6);
            color: #9ab3d9;
            font-weight: 500;
            font-size: 16px;
            border-bottom: 1px solid #2a3550;
        }}

        .trains-table td {{
            padding: 22px 20px;
            border-bottom: 1px solid #1e2840;
            color: #eef5ff;
            font-size: 18px;
        }}

        .train-row {{
            transition: all 0.2s;
        }}
        
        .train-row:hover {{
            background: rgba(50, 120, 200, 0.15);
        }}

        .minutes {{
            font-family: 'Courier New', monospace;
            font-size: 36px;
            font-weight: bold;
            color: #f5a623;
            background: rgba(0,0,0,0.5);
            display: inline-block;
            padding: 5px 18px;
            border-radius: 40px;
            letter-spacing: 2px;
        }}

        .minutes-unit {{
            font-size: 18px;
            margin-left: 5px;
            color: #ffcd94;
        }}

        .direction {{
            font-size: 24px;
            font-weight: 500;
        }}

        .train-type {{
            display: inline-block;
            padding: 6px 18px;
            border-radius: 30px;
            font-size: 16px;
            font-weight: bold;
            text-align: center;
            min-width: 120px;
        }}

        .type-normal {{
            background: #2c4c6e;
            color: #c8e7ff;
        }}

        .type-express {{
            background: #b87c1f;
            color: #fff0c0;
        }}

        .type-special {{
            background: #9b2f4d;
            color: #ffd0dc;
        }}

        .empty-message {{
            text-align: center;
            padding: 60px;
            color: #8a9bc0;
            font-size: 22px;
        }}

        @media (max-width: 768px) {{
            .display-board {{
                padding: 16px;
            }}
            .station-name {{
                font-size: 28px;
            }}
            .nav-btn {{
                width: 40px;
                height: 40px;
                font-size: 24px;
            }}
            .settings-btn {{
                font-size: 14px;
                padding: 5px 10px;
                left: 15px;
            }}
            .station-indicator {{
                left: 90px;
                font-size: 10px;
                padding: 4px 8px;
            }}
            .minutes {{
                font-size: 24px;
                padding: 3px 12px;
            }}
            .direction {{
                font-size: 18px;
            }}
            .trains-table td {{
                padding: 14px 10px;
                font-size: 14px;
            }}
        }}
    </style>
    <script>
        let currentStationIndex = {station_index};
        let totalStations = {total_stations};
        let displayCount = localStorage.getItem('displayCount') || '3';
        
        function switchStation(delta) {{
            let newIndex = currentStationIndex + delta;
            if (newIndex >= 0 && newIndex < totalStations) {{
                currentStationIndex = newIndex;
                window.location.href = '/?station=' + currentStationIndex + '&count=' + displayCount;
            }}
        }}
        
        document.addEventListener('keydown', function(e) {{
            if (e.key === 'ArrowLeft') {{
                switchStation(-1);
            }} else if (e.key === 'ArrowRight') {{
                switchStation(1);
            }}
        }});
        
        // Get display count from URL parameters
        const urlParams = new URLSearchParams(window.location.search);
        const urlCount = urlParams.get('count');
        if (urlCount) {{
            displayCount = urlCount;
            localStorage.setItem('displayCount', displayCount);
        }}
    </script>
</head>
<body>
    <div class="display-board">
        <div class="station-header">
            <a href="/settings" class="settings-btn">⚙️ Settings</a>
            <div class="station-indicator">📌 Station {station_index_display}/{total_stations}</div>
            <div class="nav-buttons">
                <div class="nav-btn" onclick="switchStation(-1)">←</div>
                <div class="nav-btn" onclick="switchStation(1)">→</div>
            </div>
            <div class="station-name">{station_name}</div>
            <div class="station-sub">● Digital Signage ● Real-time Train Info</div>
        </div>
        <div class="info-bar">
            <span>🚆 Next {display_count} Train(s)</span>
            <span class="update-time">🕒 Updated: {update_time}</span>
        </div>
        {train_rows}
        <div class="keyboard-hint">
            💡 Tip: Press <span>←</span> for previous station, <span>→</span> for next station
        </div>
    </div>
</body>
</html>
"""

# Settings Page Template (English)
SETTINGS_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Settings - Metro Digital Sign</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
            background: #0a0e1a;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}

        .settings-container {{
            max-width: 600px;
            width: 100%;
            background: linear-gradient(145deg, #101624 0%, #0c1020 100%);
            border-radius: 40px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.5);
            border: 1px solid #2a3450;
        }}

        h1 {{
            color: #7ee0ff;
            font-size: 32px;
            margin-bottom: 30px;
            text-align: center;
            border-bottom: 2px solid #2a3450;
            padding-bottom: 15px;
        }}

        .setting-item {{
            margin-bottom: 30px;
        }}

        .setting-label {{
            display: block;
            color: #bbd4f9;
            font-size: 18px;
            margin-bottom: 10px;
            font-weight: bold;
        }}

        .setting-input {{
            width: 100%;
            padding: 12px 20px;
            font-size: 18px;
            background: #1a2035;
            border: 1px solid #2a3450;
            color: #eef5ff;
            border-radius: 12px;
            transition: all 0.3s;
        }}

        .setting-input:focus {{
            outline: none;
            border-color: #2ed15e;
            box-shadow: 0 0 10px rgba(46, 209, 94, 0.3);
        }}

        .setting-hint {{
            color: #6a7c9e;
            font-size: 14px;
            margin-top: 8px;
        }}

        .buttons {{
            display: flex;
            gap: 15px;
            margin-top: 30px;
        }}

        .btn {{
            flex: 1;
            padding: 12px 24px;
            font-size: 18px;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: bold;
        }}

        .btn-save {{
            background: #2ed15e;
            color: #0a0e1a;
        }}

        .btn-save:hover {{
            background: #1ea84a;
            transform: translateY(-2px);
        }}

        .btn-cancel {{
            background: #4a5568;
            color: #eef5ff;
        }}

        .btn-cancel:hover {{
            background: #5a6578;
            transform: translateY(-2px);
        }}

        .btn-reset {{
            background: #9b2f4d;
            color: #ffd0dc;
        }}

        .btn-reset:hover {{
            background: #7a1f3a;
        }}

        .current-value {{
            background: #1a2035;
            padding: 12px 20px;
            border-radius: 12px;
            margin-bottom: 20px;
            color: #7ee0ff;
            font-size: 16px;
            text-align: center;
        }}
        
        .info-section {{
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid #2a3450;
        }}
        
        .info-section h3 {{
            color: #9ab3d9;
            margin-bottom: 10px;
            font-size: 16px;
        }}
        
        .info-section p {{
            color: #6a7c9e;
            font-size: 14px;
            margin-bottom: 8px;
        }}
        
        .code-example {{
            background: #0a0e1a;
            padding: 10px;
            border-radius: 8px;
            font-family: monospace;
            font-size: 12px;
            margin-top: 10px;
            color: #7ee0ff;
        }}
    </style>
</head>
<body>
    <div class="settings-container">
        <h1>⚙️ System Settings</h1>
        <div class="current-value" id="currentValueDisplay">Current display count: 3 trains</div>
        <div class="setting-item">
            <label class="setting-label">📊 Number of Trains to Display</label>
            <input type="number" id="trainCount" class="setting-input" min="1" value="3" placeholder="Enter number of trains">
            <div class="setting-hint">💡 Set how many upcoming trains to show (no upper limit, default: 3)</div>
        </div>
        <div class="buttons">
            <button class="btn btn-save" onclick="saveSettings()">💾 Save Settings</button>
            <button class="btn btn-reset" onclick="resetSettings()">🔄 Reset to Default</button>
            <button class="btn btn-cancel" onclick="goBack()">↩️ Back</button>
        </div>
        <div class="info-section">
            <h3>📖 Quick Guide</h3>
            <p>• Use ← → arrow keys to switch between stations</p>
            <p>• Page auto-refreshes every 10 seconds</p>
            <p>• Only shows trains that haven't departed today</p>
            <p>• Settings are saved in your browser</p>
        </div>
    </div>

    <script>
        function loadSettings() {{
            const count = localStorage.getItem('displayCount');
            if (count) {{
                document.getElementById('trainCount').value = count;
                document.getElementById('currentValueDisplay').innerHTML = `Current display count: ${{count}} trains`;
            }} else {{
                document.getElementById('trainCount').value = '3';
                document.getElementById('currentValueDisplay').innerHTML = 'Current display count: 3 trains (default)';
            }}
        }}

        function saveSettings() {{
            let count = document.getElementById('trainCount').value;
            if (count && parseInt(count) > 0) {{
                localStorage.setItem('displayCount', count);
                window.location.href = '/?count=' + count;
            }} else {{
                alert('Please enter a valid number (greater than 0)');
            }}
        }}

        function resetSettings() {{
            localStorage.removeItem('displayCount');
            document.getElementById('trainCount').value = '3';
            document.getElementById('currentValueDisplay').innerHTML = 'Current display count: 3 trains (default)';
        }}

        function goBack() {{
            window.location.href = '/';
        }}

        loadSettings();
    </script>
</body>
</html>
"""

TRAIN_ROW_TEMPLATE = """
        <tr class="train-row">
            <td><span class="minutes">{minutes}</span><span class="minutes-unit">min</span></td>
            <td><span class="direction">➡ {direction}</span></td>
            <td>{train_type_html}</td>
        </tr>
"""

def get_local_ip():
    """Get local network IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def normalize_time(time_str):
    """Normalize time format to HH:MM"""
    try:
        if ':' in time_str:
            parts = time_str.split(':')
            hour = int(parts[0])
            minute = int(parts[1])
            return f"{hour:02d}:{minute:02d}"
    except:
        pass
    return time_str

def is_time_string(s):
    """Check if string is a time format (supports H:MM or HH:MM)"""
    if ':' not in s:
        return False
    parts = s.split(':')
    if len(parts) != 2:
        return False
    try:
        hour = int(parts[0])
        minute = int(parts[1])
        return 0 <= hour <= 23 and 0 <= minute <= 59
    except:
        return False

def parse_all_stations(file_path):
    """
    Parse schedule.txt file, supports multiple stations
    Format:
    First line: Station name
    Following lines: Time Direction TrainTypeCode
    Stations separated by blank lines
    
    Train Type Codes: 1=Local, 2=Express, 3=Limited Express
    """
    stations = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.rstrip('\n') for line in f.readlines()]
        
        current_station = None
        current_trains = []
        
        for line in lines:
            stripped = line.strip()
            
            # Skip empty lines (station separators)
            if stripped == "":
                if current_station is not None:
                    stations.append({
                        'name': current_station,
                        'trains': current_trains
                    })
                    current_station = None
                    current_trains = []
                continue
            
            # Determine if line is station name or train data
            parts = stripped.split()
            
            # Train data should start with time format and have at least 3 fields
            if len(parts) >= 3 and is_time_string(parts[0]):
                # This is train data
                time_str = normalize_time(parts[0])
                direction = parts[1]
                train_type_code = parts[2]
                if current_station is not None:
                    current_trains.append({
                        'time': time_str,
                        'direction': direction,
                        'type_code': train_type_code
                    })
                else:
                    # No station name yet, create default
                    current_station = "Unknown Station"
                    current_trains.append({
                        'time': time_str,
                        'direction': direction,
                        'type_code': train_type_code
                    })
            else:
                # This is a station name
                if current_station is not None:
                    stations.append({
                        'name': current_station,
                        'trains': current_trains
                    })
                current_station = stripped
                current_trains = []
        
        # Add the last station
        if current_station is not None:
            stations.append({
                'name': current_station,
                'trains': current_trains
            })
        
        # If no stations found, create a default one
        if not stations:
            stations = [{'name': 'No Station Configured', 'trains': []}]
            
    except Exception as e:
        print(f"Failed to read file: {e}")
        stations = [{'name': 'Read Error', 'trains': []}]
    
    return stations

def calculate_minutes_until(train_time_str):
    """
    Calculate minutes until train departure
    Only shows trains that haven't departed today
    Returns None if train time has passed
    """
    try:
        now = datetime.now()
        train_hour, train_min = map(int, train_time_str.split(':'))
        train_dt = now.replace(hour=train_hour, minute=train_min, second=0, microsecond=0)
        
        # If train time <= current time, it has already departed
        if train_dt <= now:
            return None
        
        diff = train_dt - now
        minutes = int(diff.total_seconds() // 60)
        return minutes
    except:
        return None

def get_train_type_html(code):
    """Return HTML for train type based on code"""
    code = str(code).strip()
    if code == '1':
        return '<span class="train-type type-normal">🚇 Local Train</span>'
    elif code == '2':
        return '<span class="train-type type-express">⚡ Express</span>'
    elif code == '3':
        return '<span class="train-type type-special">🔥 Limited Express</span>'
    else:
        return '<span class="train-type">🚆 Regular Train</span>'

def generate_html(station_index=0, display_count=3):
    """Generate complete HTML page content"""
    stations = parse_all_stations(DATA_FILE)
    total_stations = len(stations)
    
    # Ensure valid index
    if station_index < 0:
        station_index = 0
    if station_index >= total_stations:
        station_index = total_stations - 1
    
    current_station = stations[station_index]
    station_name = current_station['name']
    trains = current_station['trains']
    
    # Calculate remaining minutes for each train, keep only today's upcoming trains
    train_list = []
    for t in trains:
        minutes_left = calculate_minutes_until(t['time'])
        if minutes_left is not None:
            train_list.append({
                'minutes': minutes_left,
                'direction': t['direction'],
                'type_code': t['type_code'],
                'raw_time': t['time']
            })
    
    # Sort by remaining time
    train_list.sort(key=lambda x: x['minutes'])
    
    # Apply display count setting
    try:
        show_count = int(display_count)
        if show_count < 1:
            show_count = 3
    except:
        show_count = 3
    
    nearest_trains = train_list[:show_count]
    
    # Generate table rows
    if nearest_trains:
        rows_html = '<table class="trains-table">\n<thead>\n<tr>\n<th>🚦 Arrival In</th>\n<th>📍 Destination</th>\n<th>🏷️ Train Type</th>\n</tr>\n</thead>\n<tbody>'
        for tr in nearest_trains:
            minutes_display = tr['minutes']
            if minutes_display <= 0:
                minutes_display = "Arriving"
            else:
                minutes_display = str(minutes_display)
            row = TRAIN_ROW_TEMPLATE.format(
                minutes=minutes_display,
                direction=tr['direction'],
                train_type_html=get_train_type_html(tr['type_code'])
            )
            rows_html += row
        rows_html += '</tbody>\n</table>'
    else:
        if len(train_list) == 0:
            rows_html = '<div class="empty-message">⚠️ No more trains today<br>Please check other stations or wait for tomorrow</div>'
        else:
            rows_html = f'<div class="empty-message">⚠️ Only {len(train_list)} train(s) available today, but you requested to show {show_count}</div>'
    
    update_time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    station_index_display = station_index + 1
    
    full_html = HTML_TEMPLATE.format(
        station_name=station_name,
        station_index=station_index,
        total_stations=total_stations,
        station_index_display=station_index_display,
        update_time=update_time_str,
        train_rows=rows_html,
        display_count=show_count
    )
    return full_html

class SubwayHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP request handler"""
    def do_GET(self):
        # Parse URL parameters
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        
        # Handle settings page
        if parsed_path.path == '/settings':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(SETTINGS_TEMPLATE.encode('utf-8'))
            return
        
        # Handle main page
        if parsed_path.path == '/' or parsed_path.path == '/index.html':
            # Get station index parameter
            station_index = 0
            if 'station' in query_params:
                try:
                    station_index = int(query_params['station'][0])
                except ValueError:
                    station_index = 0
            
            # Get display count parameter
            display_count = 3
            if 'count' in query_params:
                try:
                    display_count = int(query_params['count'][0])
                    if display_count < 1:
                        display_count = 3
                except ValueError:
                    display_count = 3
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            html_content = generate_html(station_index, display_count)
            self.wfile.write(html_content.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')
    
    def log_message(self, format, *args):
        print(f"[Access] {self.address_string()} - {format % args}")

def start_server(port):
    """Start the HTTP server"""
    with socketserver.TCPServer(("", port), SubwayHandler) as httpd:
        print(f"✅ Metro Digital Sign Service Started")
        print(f"📡 Network Access: http://{get_local_ip()}:{port}")
        print(f"🌐 Local Access: http://127.0.0.1:{port}")
        print(f"📄 Data File: {DATA_FILE}")
        print(f"⚙️  Settings: http://{get_local_ip()}:{port}/settings")
        print(f"💡 Tip: Use ← → arrow keys to switch stations")
        print(f"⏹️  Press Ctrl+C to stop\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Service stopped")

def create_sample_data():
    """Create a sample schedule.txt file if it doesn't exist"""
    import os
    if not os.path.exists(DATA_FILE):
        sample = """Qingcheng Station
6:17 To Guangzhou Baiyun 1
06:23 To Guangzhou Baiyun 2
08:25 To Guangzhou Baiyun 2
17:46 To Guangzhou Baiyun 2"""
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            f.write(sample)
        print(f"📝 Sample data file created: {DATA_FILE}")

if __name__ == "__main__":
    create_sample_data()
    start_server(PORT)
