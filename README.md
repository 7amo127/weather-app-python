# ⛅ Weather App

A beautiful, real-time desktop weather application built with **Python** and **Tkinter**.  
No API key required — powered by the free & open-source [Open-Meteo](https://open-meteo.com) API.


---

## 📸 Preview

> Search any city in the world and get instant weather data with a clean dark UI.

---

## ✨ Features

- 🌍 **Search any city** in the world by name
- 🌡️ **Current weather** — temperature, feels-like, humidity, wind speed, precipitation
- 📅 **7-day forecast** — daily high/low temps, weather conditions, and rain amounts
- 🎨 **Color-coded temperatures** — orange for hot (≥30°C), indigo for cold (≤10°C)
- 🌤 **Weather icons** based on WMO weather codes
- ⚡ **Non-blocking search** — runs in a background thread, GUI stays responsive
- 🔑 **No API key needed** — completely free to use

---

## 🛠️ Requirements

- Python 3.8 or higher
- `tkinter` (usually pre-installed with Python)

> No third-party packages needed — uses only Python's standard library!

---

## 🚀 Installation & Run

### Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/weather-app.git
cd weather-app
```

### Run directly with Python

```bash
python weather_app.py
```

#### On Kali Linux / Debian — install tkinter if missing:

```bash
sudo apt install python3-tk -y
python3 weather_app.py
```

---

## 📦 Build as a Desktop App

### 🪟 Windows — Build `.exe`

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name WeatherApp weather_app.py
```

Your executable will be at:
```
dist/WeatherApp.exe
```

Double-click to run — **no Python installation required** on the target machine.

---

### 🐧 Linux (Kali / Ubuntu / Debian) — Build binary

```bash
pip install pyinstaller --break-system-packages
pyinstaller --onefile --windowed --name WeatherApp weather_app.py
```

Run your binary:
```bash
./dist/WeatherApp
```

#### ➕ Add to app launcher (optional)

```bash
# Move binary to system path
sudo cp dist/WeatherApp /usr/local/bin/WeatherApp
sudo chmod +x /usr/local/bin/WeatherApp

# Create .desktop entry
sudo nano /usr/share/applications/weatherapp.desktop
```

Paste the following:

```ini
[Desktop Entry]
Name=Weather App
Comment=Real-time weather forecasts
Exec=/usr/local/bin/WeatherApp
Icon=weather-clear
Terminal=false
Type=Application
Categories=Utility;
```

Then refresh the app menu:
```bash
sudo update-desktop-database
```

Now the app appears in your application launcher like any installed program ✅

---

## 🏗️ Project Structure

```
weather-app/
│
├── weather_app.py      # Main application file
└── README.md           # This file
```

---

## 🌐 API Used

| Service | Purpose | Cost |
|---------|---------|------|
| [Open-Meteo Geocoding API](https://open-meteo.com/en/docs/geocoding-api) | Convert city name → coordinates | Free |
| [Open-Meteo Forecast API](https://open-meteo.com/en/docs) | Fetch current & 7-day weather | Free |

Open-Meteo is an open-source weather API — no registration, no API key, no limits for personal use.

---

## 🎨 UI Design

| Element | Detail |
|---------|--------|
| Theme | Dark navy (`#0f172a`) |
| Accent | Sky blue (`#38bdf8`) |
| Font | Georgia + Helvetica |
| Cards | Slate (`#1e293b`) |
| Hot temp | Orange (`#f97316`) |
| Cold temp | Indigo (`#818cf8`) |

---

## 📋 How It Works

1. User types a city name and hits **Search** or **Enter**
2. App calls the **Open-Meteo Geocoding API** to convert the city name to coordinates
3. Coordinates are sent to the **Open-Meteo Forecast API** to fetch weather data
4. Results are rendered in the GUI — current conditions + 7-day forecast
5. All network calls run in a **background thread** to keep the UI responsive

---

## 🤝 Contributing

Pull requests are welcome! Feel free to:
- Add more weather details (UV index, sunrise/sunset, etc.)
- Add unit toggle (°C / °F)
- Add weather history charts
- Improve the UI design

---

## 📄 License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

---

## 👤 Author

Made with ❤️ by **[YOUR_NAME](https://github.com/YOUR_USERNAME)**

> If you found this useful, give it a ⭐ on GitHub!
