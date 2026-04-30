# Metro Digital Sign System - User Manual

## 📋 Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage Guide](#usage-guide)
5. [Features](#features)
6. [Troubleshooting](#troubleshooting)
7. [FAQ](#faq)

---

## Overview

The Metro Digital Sign System is a web-based application that displays real-time train departure information on a digital sign board, similar to those found in subway stations. The system runs on your local computer and can be accessed by any device on the same network.

### Key Features
- 🚇 Real-time train departure display
- 🎯 Automatic calculation of waiting time
- 🔄 Multi-station support with keyboard navigation
- ⚙️ Customizable display settings
- 🌐 Network-accessible (LAN)
- 💾 Settings persist in browser

---

## Installation

### System Requirements
- **Operating System**: Windows 7/8/10/11, macOS, or Linux
- **Python Version**: Python 3.6 or higher
- **Network**: Local network access (optional, for other devices)

### Step-by-Step Installation

#### 1. Install Python
If you don't have Python installed:
- Download from [python.org](https://www.python.org/downloads/)
- During installation, check "Add Python to PATH"
- Verify installation: Open Command Prompt and type `python --version`

#### 2. Download the Program
Save the code as `subway_display_en.py` in a folder of your choice.

#### 3. Create Data File
Create a `schedule.txt` file in the same folder as the program.

---

## Configuration

### schedule.txt File Format

The data file uses a simple text format. Each station is defined with its name followed by train schedules.

#### Basic Format:
```
Station Name
HH:MM Direction TrainType
HH:MM Direction TrainType
HH:MM Direction TrainType

Next Station Name
HH:MM Direction TrainType
HH:MM Direction TrainType
```

#### Field Explanations:

| Field | Description | Example |
|-------|-------------|---------|
| Station Name | Name of the station/platform | Qingcheng Station |
| Time | Departure time (24-hour format) | 06:23 or 6:23 |
| Direction | Destination or route | To Guangzhou Baiyun |
| Train Type | 1=Local, 2=Express, 3=Limited Express | 1, 2, or 3 |

#### Examples:

**Single Station Example:**
```
Qingcheng Station
6:17 To Guangzhou Baiyun 1
06:23 To Guangzhou Baiyun 2
08:25 To Guangzhou Baiyun 2
17:46 To Guangzhou Baiyun 2
```

**Multiple Stations (separated by blank lines):**
```
Qingcheng Station
6:17 To Guangzhou Baiyun 1
06:23 To Guangzhou Baiyun 2
08:25 To Guangzhou Baiyun 2

Olinpic Center Station
7:00 To Airport 2
08:30 To Airport 3
18:00 To Airport 1

South Station
7:20 To Central Park 1
09:00 To Central Park 2
19:30 To Central Park 3
```

#### Important Notes:
- Blank lines separate different stations
- Time format accepts both `6:23` and `06:23`
- Train type codes must be 1, 2, or 3 only
- Station names can include spaces, numbers, and special characters

---

## Usage Guide

### Starting the Program

1. **Open Command Prompt/Terminal**
   - Windows: Press `Win + R`, type `cmd`, press Enter
   - Navigate to your program folder: `cd path\to\your\folder`

2. **Run the program:**
   ```bash
   python subway_display_en.py
   ```

3. **You should see:**
   ```
   ✅ Metro Digital Sign Service Started
   📡 Network Access: http://192.168.1.100:8080
   🌐 Local Access: http://127.0.0.1:8080
   📄 Data File: schedule.txt
   ⚙️  Settings: http://192.168.1.100:8080/settings
   💡 Tip: Use ← → arrow keys to switch stations
   ⏹️  Press Ctrl+C to stop
   ```

### Accessing the Display

#### On the same computer:
- Open any web browser (Chrome, Firefox, Edge, Safari)
- Type: `http://127.0.0.1:8080` or `http://localhost:8080`

#### On other devices (phone, tablet, another computer):
- Ensure devices are connected to the same Wi-Fi network
- Open browser and enter the Network Access address (e.g., `http://192.168.1.100:8080`)

### Using the Interface

#### Navigation
- **← Arrow Key**: Switch to previous station
- **→ Arrow Key**: Switch to next station
- **Click buttons**: Use on-screen ← → buttons

#### Display Information
- **Station Name**: Large green header showing current station
- **Arrival Time**: Minutes until train arrives
- **Destination**: Train's final destination
- **Train Type**: Color-coded tag (Local/Express/Limited Express)
- **Update Time**: When the information was last refreshed

#### Settings
1. Click the **⚙️ Settings** button in the top-left corner
2. Enter the number of trains you want to display
3. Click **Save Settings**
4. The page will reload with your new settings

### Auto-Refresh
The page automatically refreshes every 10 seconds to show updated waiting times.

---

## Features

### 1. Real-time Waiting Time Calculation
- Automatically calculates minutes until each train departs
- Only shows trains that haven't departed today
- "Arriving" displayed for trains arriving immediately

### 2. Multi-Station Support
- Switch between different stations using arrow keys
- Each station can have its own schedule
- Station indicator shows current position

### 3. Customizable Display
- Choose how many upcoming trains to display
- Settings saved in browser (survives page refresh)
- No upper limit on display count

### 4. Train Type Recognition
| Code | Type | Color | Description |
|------|------|-------|-------------|
| 1 | Local Train | Blue | Stops at all stations |
| 2 | Express | Orange | Stops at major stations only |
| 3 | Limited Express | Red | Fewer stops, faster service |

### 5. Network Accessibility
- Access from any device on the same network
- Works on phones, tablets, smart TVs, etc.
- No additional software needed on client devices

---

## Troubleshooting

### Problem: Program won't start

**Possible causes and solutions:**

1. **Python not installed**
   - Install Python from python.org
   - Make sure to check "Add Python to PATH"

2. **Port already in use**
   - Change PORT number in the code (line 10)
   - Example: `PORT = 8081`

3. **Permission denied**
   - Run Command Prompt as Administrator
   - Choose a different folder (not system-protected)

### Problem: No trains displayed

**Check:**
1. `schedule.txt` exists in the same folder
2. File format is correct (no extra spaces)
3. Train times are in the future
4. Station names don't have blank lines inside

### Problem: Wrong waiting times

**Note:** The system calculates based on your computer's clock
- Ensure your system time is correct
- The program uses 24-hour format (doesn't support AM/PM)

### Problem: Other devices can't access

**Check:**
1. Devices are on the same Wi-Fi network
2. Windows Firewall isn't blocking Python
   - Go to Windows Security → Firewall → Allow an app
   - Add Python to allowed apps
3. Use the correct IP address (shown when starting)

### Problem: Settings not saving

**Cause:** Browser localStorage is disabled or cleared
**Solution:**
- Enable cookies/localStorage in browser
- Settings are browser-specific (different browsers have different settings)

---

## FAQ

### Q1: Can I use 12-hour time format (AM/PM)?
**A:** No, only 24-hour format is supported. Use 06:00 instead of 6:00 AM.

### Q2: What happens if a train time has passed?
**A:** The system automatically hides trains that have already departed today. It doesn't show tomorrow's trains.

### Q3: Can I run this on a Raspberry Pi?
**A:** Yes! Python runs on Raspberry Pi. Use the same code.

### Q4: How do I stop the program?
**A:** Press `Ctrl + C` in the Command Prompt window.

### Q5: Can I change the refresh rate?
**A:** Yes, find `<meta http-equiv="refresh" content="10">` in the HTML template and change the number (in seconds).

### Q6: Can I customize colors and layout?
**A:** Yes, modify the CSS styles in the HTML_TEMPLATE variable in the Python file.

### Q7: How many stations can I have?
**A:** No limit! Just separate them with blank lines in schedule.txt.

### Q8: Will it work without internet?
**A:** Yes! The system runs entirely on your local computer. No internet required.

### Q9: Can I use emojis in station names?
**A:** Yes, as long as your text file is saved with UTF-8 encoding.

### Q10: How to automatically start on boot?
**A:** 
- **Windows**: Create a .bat file and add to Startup folder
- **macOS/Linux**: Use crontab or systemd

---

## Advanced Configuration

### Changing the Port
Edit line 10 in the Python file:
```python
PORT = 8080  # Change to any available port (8000-9000 recommended)
```

### Changing Auto-Refresh Rate
Find in HTML_TEMPLATE:
```html
<meta http-equiv="refresh" content="10">  # Change 10 to desired seconds
```

### Adding More Train Types
Modify the `get_train_type_html()` function:
```python
elif code == '4':
    return '<span class="train-type">🚀 Bullet Train</span>'
```

### Multi-language Support
- HTML_TEMPLATE contains all visible text
- Translate the strings to your preferred language
- Keep the variable names (e.g., {station_name}) unchanged

---

## Support

### File Locations
- **Program**: `subway_display_en.py`
- **Data**: `schedule.txt` (same folder as program)
- **Settings**: Stored in browser localStorage

### Command Line Arguments (if added)
Currently no command line arguments. To add:
1. Import sys: `import sys`
2. Parse sys.argv for custom port or file path

### Log Files
The program outputs to console only. To save logs:
```bash
python subway_display_en.py > log.txt 2>&1
```

---

## Version History

**Version 1.0** (2024)
- Initial release
- Basic station display
- Keyboard navigation
- Settings page
- English interface

---

## License

This software is provided free for personal and commercial use. You may modify and distribute it freely.

---

## Credits

Created for metro/signage applications. Uses only Python standard library - no third-party dependencies!

---

**Thank you for using Metro Digital Sign System!** 🚇
