

import tkinter as tk
from tkinter import messagebox
import urllib.request
import json
import threading

# ── Geo-coding: city name → lat/lon (Open-Meteo geocoding) ──────────────────
def geocode(city: str):
    url = (
        f"https://geocoding-api.open-meteo.com/v1/search"
        f"?name={urllib.parse.quote(city)}&count=1&language=en&format=json"
    )
    with urllib.request.urlopen(url, timeout=8) as r:
        data = json.loads(r.read())
    results = data.get("results")
    if not results:
        return None
    r = results[0]
    return r["name"], r["country"], r["latitude"], r["longitude"]

# ── Weather fetch ────────────────────────────────────────────────────────────
def fetch_weather(lat: float, lon: float):
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,"
        f"wind_speed_10m,weather_code,precipitation"
        f"&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum"
        f"&timezone=auto&forecast_days=7"
    )
    with urllib.request.urlopen(url, timeout=8) as r:
        return json.loads(r.read())

import urllib.parse   # needed above

# ── WMO weather-code → emoji + label ────────────────────────────────────────
def wmo_label(code: int):
    table = {
        0: ("☀️", "Clear sky"),
        1: ("🌤", "Mainly clear"), 2: ("⛅", "Partly cloudy"), 3: ("☁️", "Overcast"),
        45: ("🌫", "Fog"), 48: ("🌫", "Icy fog"),
        51: ("🌦", "Light drizzle"), 53: ("🌦", "Drizzle"), 55: ("🌧", "Dense drizzle"),
        61: ("🌧", "Slight rain"), 63: ("🌧", "Rain"), 65: ("🌧", "Heavy rain"),
        71: ("🌨", "Slight snow"), 73: ("🌨", "Snow"), 75: ("❄️", "Heavy snow"),
        80: ("🌦", "Rain showers"), 81: ("🌧", "Showers"), 82: ("⛈", "Heavy showers"),
        95: ("⛈", "Thunderstorm"), 96: ("⛈", "Thunderstorm+hail"), 99: ("⛈", "Heavy T-storm"),
    }
    return table.get(code, ("🌡", "Unknown"))

# ── Day name ─────────────────────────────────────────────────────────────────
from datetime import datetime

def day_name(date_str: str, i: int):
    if i == 0: return "Today"
    if i == 1: return "Tomorrow"
    return datetime.strptime(date_str, "%Y-%m-%d").strftime("%A")

# ════════════════════════════════════════════════════════════════════════════
#   GUI
# ════════════════════════════════════════════════════════════════════════════

BG        = "#0f172a"   # deep navy
CARD      = "#1e293b"   # slate card
ACCENT    = "#38bdf8"   # sky-blue
TEXT_PRI  = "#f1f5f9"
TEXT_SEC  = "#94a3b8"
HOT       = "#f97316"   # orange highlight
COLD      = "#818cf8"   # indigo highlight
RADIUS    = 16

class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather  ⛅")
        self.geometry("540x780")
        self.resizable(False, False)
        self.configure(bg=BG)
        self._build_ui()

    # ── Search bar ───────────────────────────────────────────────────────────
    def _build_ui(self):
        # top gradient strip (canvas trick)
        strip = tk.Canvas(self, height=6, bg=BG, highlightthickness=0)
        strip.pack(fill="x")
        strip.create_rectangle(0, 0, 540, 6, fill=ACCENT, outline="")

        # title
        tk.Label(self, text="⛅  Weather", font=("Georgia", 22, "bold"),
                 bg=BG, fg=TEXT_PRI).pack(pady=(18, 4))
        tk.Label(self, text="Real-time forecasts — no API key needed",
                 font=("Helvetica", 10), bg=BG, fg=TEXT_SEC).pack()

        # search row
        row = tk.Frame(self, bg=BG)
        row.pack(pady=18, padx=30, fill="x")
        self.entry = tk.Entry(row, font=("Helvetica", 13), bg=CARD, fg=TEXT_PRI,
                              insertbackground=ACCENT, relief="flat",
                              bd=0, highlightthickness=2,
                              highlightcolor=ACCENT, highlightbackground="#334155")
        self.entry.pack(side="left", fill="x", expand=True, ipady=10, ipadx=10)
        self.entry.insert(0, "Cairo")
        self.entry.bind("<Return>", lambda e: self._search())

        btn = tk.Button(row, text="Search", font=("Helvetica", 12, "bold"),
                        bg=ACCENT, fg="#0f172a", relief="flat", bd=0,
                        activebackground="#7dd3fc", activeforeground="#0f172a",
                        cursor="hand2", command=self._search)
        btn.pack(side="left", padx=(8, 0), ipady=10, ipadx=14)

        # scrollable body
        self.body = tk.Frame(self, bg=BG)
        self.body.pack(fill="both", expand=True, padx=20)

        # status / spinner label
        self.status = tk.Label(self.body, text="", font=("Helvetica", 11),
                               bg=BG, fg=TEXT_SEC)
        self.status.pack(pady=6)

        # current weather card
        self.cur_card = tk.Frame(self.body, bg=CARD, pady=18, padx=20)
        # forecast row
        self.fc_frame = tk.Frame(self.body, bg=BG)

    # ── Trigger search in background thread ──────────────────────────────────
    def _search(self):
        city = self.entry.get().strip()
        if not city:
            return
        self.status.config(text="🔍  Searching…")
        self._clear_cards()
        threading.Thread(target=self._load, args=(city,), daemon=True).start()

    def _load(self, city):
        try:
            geo = geocode(city)
            if not geo:
                self.after(0, lambda: self.status.config(text="❌  City not found."))
                return
            name, country, lat, lon = geo
            data = fetch_weather(lat, lon)
            self.after(0, lambda: self._render(name, country, data))
        except Exception as e:
            self.after(0, lambda: self.status.config(text=f"⚠️  Error: {e}"))

    # ── Render results ────────────────────────────────────────────────────────
    def _clear_cards(self):
        for w in self.cur_card.winfo_children():
            w.destroy()
        for w in self.fc_frame.winfo_children():
            w.destroy()

    def _render(self, name, country, data):
        self.status.config(text="")
        cur = data["current"]
        daily = data["daily"]

        emoji, label = wmo_label(cur["weather_code"])
        temp = cur["temperature_2m"]
        feels = cur["apparent_temperature"]
        hum = cur["relative_humidity_2m"]
        wind = cur["wind_speed_10m"]
        precip = cur["precipitation"]
        temp_color = HOT if temp >= 30 else (COLD if temp <= 10 else TEXT_PRI)

        # ── Current card ─────────────────────────────────────────────────────
        self.cur_card.pack(fill="x", pady=(0, 12))

        tk.Label(self.cur_card, text=f"{name},  {country}",
                 font=("Georgia", 15, "bold"), bg=CARD, fg=ACCENT).pack(anchor="w")

        mid = tk.Frame(self.cur_card, bg=CARD)
        mid.pack(fill="x", pady=(10, 0))

        tk.Label(mid, text=emoji, font=("Segoe UI Emoji", 52), bg=CARD).pack(side="left")

        right = tk.Frame(mid, bg=CARD)
        right.pack(side="left", padx=20)
        tk.Label(right, text=f"{temp:.1f}°C", font=("Georgia", 42, "bold"),
                 bg=CARD, fg=temp_color).pack(anchor="w")
        tk.Label(right, text=label, font=("Helvetica", 13),
                 bg=CARD, fg=TEXT_SEC).pack(anchor="w")

        stats = tk.Frame(self.cur_card, bg=CARD)
        stats.pack(fill="x", pady=(14, 0))
        for icon, val in [("🌡 Feels", f"{feels:.1f}°C"),
                          ("💧 Humidity", f"{hum}%"),
                          ("💨 Wind", f"{wind} km/h"),
                          ("🌧 Precip", f"{precip} mm")]:
            col = tk.Frame(stats, bg="#263348", padx=10, pady=6)
            col.pack(side="left", expand=True, fill="x", padx=4)
            tk.Label(col, text=icon, font=("Helvetica", 9), bg="#263348",
                     fg=TEXT_SEC).pack()
            tk.Label(col, text=val, font=("Helvetica", 11, "bold"), bg="#263348",
                     fg=TEXT_PRI).pack()

        # ── 7-day forecast ────────────────────────────────────────────────────
        tk.Label(self.body, text="7-Day Forecast", font=("Georgia", 13, "bold"),
                 bg=BG, fg=TEXT_PRI).pack(anchor="w", pady=(4, 6))
        self.fc_frame.pack(fill="x")

        dates  = daily["time"]
        codes  = daily["weather_code"]
        maxts  = daily["temperature_2m_max"]
        mints  = daily["temperature_2m_min"]
        precs  = daily["precipitation_sum"]

        for i in range(7):
            em, lb = wmo_label(codes[i])
            fc = tk.Frame(self.fc_frame, bg=CARD, pady=8, padx=10)
            fc.pack(fill="x", pady=3)

            tk.Label(fc, text=day_name(dates[i], i),
                     font=("Helvetica", 11, "bold"), width=10, anchor="w",
                     bg=CARD, fg=TEXT_PRI).pack(side="left")
            tk.Label(fc, text=em + " " + lb,
                     font=("Segoe UI Emoji", 10), width=22, anchor="w",
                     bg=CARD, fg=TEXT_SEC).pack(side="left")

            hi_col = HOT if maxts[i] >= 30 else TEXT_PRI
            lo_col = COLD if mints[i] <= 10 else TEXT_SEC
            tk.Label(fc, text=f"↑{maxts[i]:.0f}°",
                     font=("Helvetica", 11, "bold"), bg=CARD, fg=hi_col).pack(side="right", padx=4)
            tk.Label(fc, text=f"↓{mints[i]:.0f}°",
                     font=("Helvetica", 11), bg=CARD, fg=lo_col).pack(side="right", padx=4)
            if precs[i] > 0:
                tk.Label(fc, text=f"🌧 {precs[i]:.1f}mm",
                         font=("Helvetica", 9), bg=CARD, fg="#7dd3fc").pack(side="right", padx=4)

        # footer
        tk.Label(self.body, text="Data: Open-Meteo (open-meteo.com) • free & open-source",
                 font=("Helvetica", 8), bg=BG, fg="#475569").pack(pady=10)

# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()