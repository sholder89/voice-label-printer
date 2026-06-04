# 🖨️ Voice Label Printer

Print labels with your voice. Say *"Alexa, print kitchen supplies"* and a label rolls out of your NIIMBOT printer — complete with an automatically matched emoji icon.

---

## How It Works

```
You (voice) → Alexa Skill → AWS Lambda → Relay Server (VPS) → Windows Client → NIIMBOT Printer
```

1. You speak a command to Alexa.
2. An AWS Lambda function posts the job to a relay server hosted on your VPS.
3. The Windows client polls the relay every few seconds, picks up the job, renders a label image, and sends it to the printer via the Windows print queue.
4. You can also type and print directly through the local web UI at `http://localhost:5000`.

---

## Features

### 🖨️ Printing
- Prints to any Windows printer — tested with **NIIMBOT B21 / Y813BT** via Bluetooth
- 203 DPI rendering via Pillow — what you see in the preview is exactly what prints
- Multiple label sizes: **2×1**, **4×2**, **4×6**, **3×2**, **2×0.5** (inches)
- Print multiple copies (up to 10) from the web UI

### 😀 Automatic Emoji Icons
- Type (or say) any label text and the app automatically detects a matching emoji icon
- Over **2,000 keywords** covering household items, sports, hobbies, professions, food, nature, and more
- Icons appear to the left of the label text
- Supports **ZWJ emoji sequences** (e.g. 🧑‍✈️ pilot, 🧑‍🔬 scientist, 🐦‍⬛ crow) rendered correctly via HarfBuzz + FreeType
- Icons can be toggled on/off per label or globally
- **Longest-match detection** — "polar bear" correctly picks 🐻‍❄️ over just 🐻

### 🎨 Style Presets
Choose a style to completely change the look of a label:

| Group | Preset | Description |
|-------|--------|-------------|
| Typography | **None** | Use your current font/border settings |
| Typography | **Minimal** | Clean Segoe UI font with thin border |
| Typography | **Bold** | Impact font, thick border |
| Typography | **Elegant** | Georgia serif font, double border |
| Typography | **Retro Typewriter** | Courier monospace, dashed border |
| Layouts | **Address Label** | Left-aligned multi-line address format |
| Layouts | **Price Tag** | Eyelet hole on left, vertical divider, text on right |
| Layouts | **Cassette** | Black end blocks, white center spine |
| Layouts | **QR Code** | Generates a scannable QR code from the label text |
| Themed | **Windows 95** | Classic raised-button gray UI chrome |
| Themed | **Blueprint** | Black background, white grid lines |
| Themed | **Warning** | ⚠ hazard header, diagonal stripes, icon + body text |

### 🔤 Fonts & Weights
- **Font styles:** Standard (Arial), Enhanced (Segoe UI), Impact, Serif (Georgia), Narrow (Arial Narrow), Mono (Courier New), Burbank (Burbank Big Condensed Bold)
- **Font weights:** Normal, Bold, Italic, Bold Italic — each with proper fallback fonts
- **W95FA pixel font** used for Windows 95 style
- Text automatically scales to fill the available label area — tries every line-break combination to find the biggest font size that fits

### 🔲 Borders
Built-in border styles: **None, Thin, Thick, Double, Dashed, Rounded, Corners**

**Custom image borders** — drop any PNG/WebP/JPG named `border_<name>.png` into `client/images/` and it appears automatically in the dropdown after a restart.

### 🔡 Text Case
Transform label text automatically: **None, UPPERCASE, lowercase, Title Case, Sentence case**

### 📜 Print History
- Last 100 prints stored in `%APPDATA%\LabelPrinter\history.json`
- Paginated display (10 per page)
- **Hover** over a history row to preview the label image
- **Reprint** any past label with its original settings
- **Load** a past label back into the form to edit it
- **Delete** individual entries or **Clear All**

### 📬 Address Labels
- Dedicated address form with Name, Line 1, Line 2, City/State/ZIP fields
- **Save addresses** for quick reprinting later
- Uses the Address Label style preset automatically

### 🌙 Dark Mode
Full dark/light mode toggle with persistent preference. CSS custom properties handle theming throughout.

### 🔔 Notifications
Optional Telegram notifications on every print. Configure via `SHOUTRRR_URL` environment variable:
```
telegram://<bot_token>@telegram?chats=<chat_id>
```

---

## Voice Commands (Alexa)

| What you say | What happens |
|---|---|
| *"Alexa, ask label printer to print kitchen supplies"* | Prints a label |
| *"Alexa, ask label printer to set style to warning"* | Changes style preset |
| *"Alexa, ask label printer to set size to four by two"* | Changes label size |
| *"Alexa, ask label printer to set font to burbank"* | Changes font style |
| *"Alexa, ask label printer to set border to double"* | Changes border style |
| *"Alexa, ask label printer to set font weight to italic"* | Changes font weight |
| *"Alexa, ask label printer to turn icons off"* | Disables emoji icons |
| *"Alexa, ask label printer to set text to uppercase"* | Changes text case |

---

## Setup

### Requirements
- Windows 10/11 (printing uses the Windows GDI/win32 APIs)
- Python 3.11+
- A NIIMBOT or similar label printer installed as a Windows printer

### Client (Windows)

1. Clone the repo and `cd` into `client/`
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your values:
   ```
   RELAY_URL=https://your-relay-server.com
   LABEL_TOKEN=your-secret-token
   ```
4. Run:
   ```
   python app.py
   ```
   The web UI opens at `http://localhost:5000` and a printer icon appears in the system tray.

**Optional fonts** — place these in `C:\Users\<you>\AppData\Local\Microsoft\Windows\Fonts\`:
- `BurbankBigCondensed-Bold.otf` — enables the Burbank font style
- `W95F.otf` (W95FA) — enables the authentic pixel font for Windows 95 style

### Server (Docker / VPS)

The relay server brokers jobs between Alexa and the Windows client.

1. Copy `server/.env.example` to `server/.env`:
   ```
   LABEL_TOKEN=your-secret-token
   ```
2. Deploy with Docker Compose:
   ```
   docker compose up -d --build
   ```

The server exposes port `5001`. Put it behind Traefik / nginx / Caddy with HTTPS.

**Cloudflare WAF** — if your domain is proxied through Cloudflare, add a WAF bypass rule (Skip action) for the Alexa webhook so it isn't challenged:
```
http.host eq "your-domain.com"
and http.user_agent eq "AlexaLabelPrinter/1.0"
and (http.request.uri.path eq "/webhook" or http.request.uri.path eq "/settings")
```

### Alexa Skill

1. Create a new custom skill in the [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask)
2. In the **JSON Editor**, paste the contents of `alexa-skill/interaction_model.json` and click **Save Model**
3. Click **Build Model**
4. Deploy `alexa-skill/lambda_function.py` to AWS Lambda (Python 3.12 runtime)
5. Set these Lambda environment variables:
   ```
   WEBHOOK_URL=https://your-relay-server.com/webhook
   SETTINGS_URL=https://your-relay-server.com/settings
   LABEL_TOKEN=your-secret-token
   ```
6. Connect the Lambda to your Alexa skill as the endpoint

---

## Environment Variables

### Client (`.env`)
| Variable | Default | Description |
|---|---|---|
| `RELAY_URL` | `https://yourserver.com` | URL of the relay server |
| `LABEL_TOKEN` | `changeme` | Shared secret — must match server and Lambda |
| `POLL_SECS` | `3` | How often to poll for new jobs (seconds) |
| `DEFAULT_PRINTER` | *(first printer found)* | Printer name to pre-select |
| `DEFAULT_SIZE` | `2x1` | Label size to pre-select |
| `DEFAULT_FONT_STYLE` | `enhanced` | Font style to pre-select |
| `DEFAULT_FONT_WEIGHT` | `bold` | Font weight to pre-select |
| `SHOUTRRR_URL` | *(empty)* | Telegram URL for print notifications |

### Server (`server/.env`)
| Variable | Description |
|---|---|
| `LABEL_TOKEN` | Shared secret — must match client and Lambda |

---

## Data Storage

All user data is stored in `%APPDATA%\LabelPrinter\` (i.e. `C:\Users\<you>\AppData\Roaming\LabelPrinter\`):

| File | Contents |
|---|---|
| `settings.json` | Current printer, size, font, border, style preset, etc. |
| `history.json` | Print history (last 100) with full render settings |
| `addresses.json` | Saved address book entries |

Settings survive restarts and app updates automatically.

---

## System Tray

The app lives in the Windows system tray when running:

| Action | Result |
|---|---|
| Double-click | Open web UI |
| Right-click → Open | Open web UI |
| Right-click → Restart | Restart the app (no new browser tab) |
| Right-click → Quit | Exit |

---

## Project Structure

```
├── client/
│   ├── app.py              # Flask web UI + background polling thread + tray icon
│   ├── printer.py          # Label rendering (Pillow) + Windows GDI printing
│   ├── emoji_data.py       # 2,000+ keyword → emoji mappings
│   ├── requirements.txt
│   ├── images/             # Drop custom border images here (border_<name>.png)
│   ├── static/             # favicon.ico, favicon.png
│   └── templates/
│       └── index.html      # Single-page web UI
├── server/
│   ├── app.py              # Flask relay server
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
├── alexa-skill/
│   ├── lambda_function.py  # AWS Lambda handler
│   └── interaction_model.json
└── make_favicon.py         # Utility: regenerates favicon from printer emoji
```

---

## Security Notes

- `LABEL_TOKEN` is sent as an `X-Token` HTTP header (not in the URL)
- `server/.env` and `client/.env` are **gitignored** — never commit them
- The relay server validates the token on every request
- The Alexa Lambda is the only external caller; all other traffic can be firewall-blocked

---

## Dependencies

### Client
| Package | Purpose |
|---|---|
| `flask` | Web UI server |
| `pillow` | Label image rendering |
| `pywin32` | Windows GDI printing + printer enumeration |
| `pystray` | System tray icon |
| `requests` | Polling the relay server |
| `qrcode[pil]` | QR Code style preset |
| `uharfbuzz` | HarfBuzz text shaping for ZWJ emoji sequences |
| `freetype-py` | FreeType rendering of color emoji bitmaps |

### Server
| Package | Purpose |
|---|---|
| `flask` | HTTP API |
| `gunicorn` | WSGI production server |
