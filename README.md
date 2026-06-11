![Voice Label Printer](client/static/logo-light.png#gh-light-mode-only)
![Voice Label Printer](client/static/logo-dark.png#gh-dark-mode-only)

> ⚠️ **Heads up:** This app is fully vibe coded. I'm a database guy, not a developer. Use at your own risk.

Print labels with your voice. Say *"Alexa, print kitchen supplies"* or *"Hey Siri, print label"* and a label rolls out of your thermal printer — complete with an automatically matched emoji icon.

---

## How It Works

```
You (voice) → Alexa Skill → AWS Lambda → Relay Server (VPS) → Windows Client → Thermal Printer
         or → Siri Shortcut ──────────────────────────────↗
```

1. You speak a command to Alexa or Siri.
2. For Alexa: an AWS Lambda function posts the job to a relay server hosted on your VPS.  
   For Siri: the Shortcut posts directly to the relay server (no IFTTT or Lambda needed).
3. The Windows client polls the relay every few seconds, picks up the job, renders a label image, and sends it to the printer via the Windows print queue.
4. You can also type and print directly through the local web UI at `http://localhost:5000` (also accessible from other devices on your network).

---

## Features

### 🖨️ Printing
- Prints to any Windows printer — tested with **NULLTONEX** Bluetooth thermal label printer and **Brother QL-710W**
- 203 DPI rendering via Pillow — what you see in the preview is exactly what prints
- Multiple label sizes: **2×1**, **4×2**, **4×6**, **3×2**, **2×0.5** (inches), **1.1×3.5**, **1.1×2.4** (Brother QL 29mm tape)
- Print multiple copies (up to 10) from the web UI

### 😀 Automatic Emoji Icons
- Type (or say) any label text and the app automatically detects a matching emoji icon
- Over **3,800 keywords** covering household items, sports, hobbies, professions, food, brands, electronic components, country flags, and more — see **[EMOJIS.md](EMOJIS.md)** for the full list
- Icons appear to the left of the label text (stacked above on portrait labels)
- Rendered via **Noto Color Emoji** (fonttools PNG extraction) with HarfBuzz + FreeType as fallback — correctly handles ZWJ sequences (🧑‍✈️ pilot, 🧑‍🔬 scientist) and country flags (🇺🇸 🇬🇧 🇯🇵 and all others)
- Icons can be toggled on/off per label or globally
- **Longest-match detection** — "polar bear" correctly picks 🐻‍❄️ over just 🐻
- **Custom emojis** — map your own keywords to any emoji on the Advanced page (🔧 icon, PC-only). Custom mappings **override** the built-in ones, pick from a searchable grid of all 1,870 emojis, and apply live to voice prints. Stored in `custom_emojis.json`.

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
| Layouts | **Barcode** | Scannable Code 128 barcode with a human-readable caption (best on wider labels) |
| Layouts | **Name Tag** | Classic "HELLO my name is" banner with the name large below |
| Layouts | **Receipt** | Centered monospace text framed by dashed rules — thermal-receipt look |
| Themed | **Windows 95** | Classic raised-button gray UI chrome |
| Themed | **Blueprint** | Black background, grey grid lines |
| Themed | **Warning** | ⚠ hazard header, diagonal stripes, icon + body text |
| Themed | **Chalkboard** | Black board with white handwriting (Ink Free) and a chalk frame |

Three quick-action buttons sit below the Style Preset dropdown:
- **🎲 Randomize** — picks a random preset, or randomises font/border/weight individually
- **↩ Default** — restores your saved default style
- **📌 Set Default** — saves the current style as your default (persists across restarts)

### 🔤 Fonts & Weights
- **Font styles:** Standard (Arial), Enhanced (Segoe UI), Impact, Serif (Georgia), Narrow (Arial Narrow), Mono (Courier New), Consolas, Bahnschrift (condensed — great for fitting more text), Burbank (Burbank Big Condensed Bold), Ink Free (handwriting)
- **Font weights:** Normal, Bold, Italic, Bold Italic — each with proper fallback fonts
- **W95FA pixel font** used for Windows 95 style
- Text automatically scales to fill the available label area — tries every line-break combination to find the biggest font size that fits

### 🔲 Borders
Built-in border styles: **None, Thin, Thick, Double, Dashed, Dotted, Wave (scalloped), Ticket (perforated), Inset (3D), Rounded, Corners**

**Custom image borders** — drop any PNG/WebP/JPG named `border_<name>.png` into `client/images/` and it appears automatically in the dropdown after a restart.

### 🔡 Text Case
Transform label text automatically: **None, UPPERCASE, lowercase, Title Case, Sentence case**

### 📜 Print History
- Last 500 prints stored in `%APPDATA%\LabelPrinter\history.json`
- Paginated display (10 per page) with windowed ellipsis page numbers
- **Hover** over a history row to preview the label image
- **Reprint** any past label with its original settings
- **Load** a past label back into the form to edit it
- **Delete** individual entries or **Clear All**

### 📬 Address Labels
- Dedicated address form with Name, Line 1, Line 2, City/State/ZIP fields
- **Save addresses** for quick reprinting later
- Uses the Address Label style preset automatically

### 🌙 Dark Mode
Full dark/light mode toggle with persistent preference. CSS custom properties handle theming throughout. The **Appearance** section of the Advanced page also offers an explicit **Light / Dark / Follow System** selector — "Follow System" tracks your OS theme.

### 🔔 Notifications
Optional Telegram notifications on every print (a message per label, with a 🎙/🖥 marker showing whether it came from voice or the UI). Configure it live from the **Advanced page** (enable toggle, bot token, chat ID, and a **Send test message** button) — no restart needed. As a fallback you can also seed credentials from the `SHOUTRRR_URL` environment variable:
```
telegram://<bot_token>@telegram?chats=<chat_id>
```
The bot token is write-only in the UI — it's never displayed back, only overwritten when you type a new one.

---

## Advanced Settings (PC-only)

Click the **🔧** icon in the header — visible **only on the PC running the client**, never from phones or other LAN devices — to open a tabbed settings page. Every option here applies live, with no restart:

| Section | What it does |
|---|---|
| **Connection** | Change the relay URL or rotate the `LABEL_TOKEN` (write-only), with a **Test connection** button |
| **Telegram** | Enable/disable print notifications and configure the bot token + chat ID |
| **Emoji Darkness** | A 0–100% slider that darkens emoji icons for faint thermal printers, with a live preview strip — preserves full grayscale detail rather than flattening to black |
| **Custom Emojis** | Map your own keywords to any emoji (searchable picker of all 1,870), with a per-row toggle to enable/disable each mapping without deleting it |
| **Custom Label Sizes** | Define named sizes in inches, mm, or cm — they appear in the Print Settings size list |
| **Appearance** | Light / Dark / Follow System theme selector |

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

## Voice Commands (Siri)

Siri control uses Apple Shortcuts — no IFTTT, no Lambda, no skill setup required. The Shortcut posts directly to the relay server.

### Setup

1. Open the **Shortcuts** app on your iPhone/iPad/Mac
2. Tap **+** to create a new shortcut, name it **"Print Label"**
3. Add these actions in order:

   **Action 1 — Ask for Input**
   - Input type: **Text**
   - Prompt: *"What should the label say?"*

   **Action 2 — Get Contents of URL**
   - URL: `https://your-relay-server.com/webhook`
   - Method: **POST**
   - Headers: add `X-Token` → `your-label-token`
   - Request Body: **JSON**
     - Add field: `value1` → select **Provided Input** from step 1

4. Tap **Done**

### Usage

Say **"Hey Siri, Print Label"** → Siri asks what to print → you reply → label prints.

You can name the shortcut anything — whatever you name it is what you say to Siri.

---

## Setup

### Requirements
- Windows 10/11 (printing uses the Windows GDI/win32 APIs)
- Python 3.11+
- Any Windows-compatible thermal label printer

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
   The web UI opens at `http://localhost:5000` and a printer icon appears in the system tray. The UI is also accessible from other devices on the same network at `http://<this-pc-ip>:5000`.

> **Tip — Advanced Settings:** `RELAY_URL` and `LABEL_TOKEN` from `.env` are just the startup defaults. Once running, click the **🔧** icon in the header (visible **only on this PC**, not from phones/other devices) to change the relay endpoint or rotate the token live — no restart, no editing `.env`. The token is write-only there: it's never displayed back, only overwritten when you type a new one. There's also a **Test connection** button to verify the endpoint + token before relying on them.

**Optional fonts** — place these in `C:\Users\<you>\AppData\Local\Microsoft\Windows\Fonts\`:
- `BurbankBigCondensed-Bold.otf` — enables the Burbank font style
- `W95F.otf` (W95FA) — enables the authentic pixel font for Windows 95 style
- `NotoColorEmoji_WindowsCompatible.ttf` — enables country flags and Unicode 15 emoji (🪼 🫎 🪿 etc.). Download from [github.com/googlefonts/noto-emoji/releases](https://github.com/googlefonts/noto-emoji/releases) — get the `WindowsCompatible` variant

### Server

The relay server brokers jobs between Alexa/Siri and the Windows client. It needs to be reachable from the internet with a public HTTPS URL. Pick whichever deployment option suits you:

---

#### Option A: Railway (easiest, free tier available)

[Railway](https://railway.app) detects the Dockerfile automatically and handles HTTPS for you — no reverse proxy setup needed.

1. Create a free account at railway.app
2. Click **New Project → Deploy from GitHub repo** and select this repo
3. Set the root directory to `server/`
4. Under **Variables**, add:
   ```
   LABEL_TOKEN=your-secret-token
   ```
5. Railway gives you a public URL like `https://voice-label-printer-production.up.railway.app` — use this as your `RELAY_URL`

---

#### Option B: Render (also easy, free tier available)

[Render](https://render.com) works similarly to Railway.

1. Create a free account at render.com
2. Click **New → Web Service**, connect your GitHub repo
3. Set the root directory to `server/`, runtime to **Docker**
4. Under **Environment**, add:
   ```
   LABEL_TOKEN=your-secret-token
   ```
5. Render gives you a public URL like `https://voice-label-printer.onrender.com` — use this as your `RELAY_URL`

> **Note:** Render's free tier spins down after inactivity, which adds a ~30 second cold start delay on the first request. Railway stays warm. Either is fine for occasional use; Railway is better if you want instant response every time.

---

#### Option C: Self-hosted VPS (Docker Compose)

If you already have a server (DigitalOcean, Linode, Vultr, etc.):

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

---

#### Option D: All-local on Windows (no cloud, no Docker)

Run the relay server **on the same Windows PC as the client** and drive it entirely from **Siri** over your home Wi-Fi. Nothing leaves your network and there's no VPS or container to maintain. This works because the server is plain Flask + SQLite — Docker is just one way to run it.

> Best for a Siri-only setup. Alexa still needs an internet-reachable server (Options A–C), since Amazon's cloud calls your webhook from outside your network.

**One-time setup:**

1. Make sure Python is installed (same requirement as the client).
2. Put your shared secret in the project-root `.env` (the client reads it too):
   ```
   LABEL_TOKEN=your-secret-token
   ```
3. Right-click **`setup-windows.ps1` → Run with PowerShell**. It adds a login auto-start shortcut (no admin needed).
   - **Firewall:** you usually don't need to touch it — Windows prompts to allow Python the first time the server accepts a connection, or your Private network already permits LAN traffic. **Only** if another device (your phone) can't reach the apps, open an **admin** PowerShell and run:
     ```
     powershell -ExecutionPolicy Bypass -File setup-windows.ps1 -Firewall
     ```
     That adds inbound rules for ports `5001` (server) and `5000` (client) on the Private profile.

**Run it:**

- **`start-all.bat`** — installs dependencies and launches both the server and client (each lives in the system tray). Use this the first time and after updates.
- After auto-start is set up, both launch automatically at login (via `run-all.bat`, which skips the dependency check for a fast boot).
- To run only the server: **`server/start-local.bat`**.

**Point Siri at it:** open the server's tray icon → **Open setup page** (or browse to `http://localhost:5001/`). It shows your PC's LAN webhook URL (e.g. `http://192.168.1.50:5001/webhook`), the exact `X-Token` header value, and copy-paste Siri Shortcut steps. Set the Shortcut's `RELAY_URL` equivalent to that LAN URL instead of a public one.

**Client config:** set the client's `RELAY_URL` to the local server:
```
RELAY_URL=http://127.0.0.1:5001
```

> ⚠️ **The client web UI (port 5000) has no password.** Anyone on your home Wi-Fi who opens `http://<your-pc-ip>:5000/` can print labels, change settings, and clear history. The relay server (port 5001) *is* protected by `LABEL_TOKEN`, but the client UI is intentionally open so you can reach it from your phone. On a trusted home network this is usually fine — but don't port-forward `5000` to the internet, and only add the firewall rule above if you actually need LAN access.

| | All-local (Option D) | Cloud (Options A–C) |
|---|---|---|
| Works with Siri | ✅ on home Wi-Fi | ✅ anywhere |
| Works with Alexa | ❌ (needs public URL) | ✅ |
| Works away from home | ❌ | ✅ |
| Cost / maintenance | none | VPS or free tier |
| HTTPS needed | no (plain HTTP on LAN) | yes |

The server DB is stored at `%APPDATA%\LabelPrinter\jobs.db` (kept out of the OneDrive-synced project folder). Local runs use Flask's built-in server via `requirements-local.txt`; the Docker image keeps using gunicorn (`requirements.txt`), which is Unix-only.

### Alexa Skill + AWS Lambda

The Alexa skill is what listens for your voice commands. When you speak, Alexa calls an AWS Lambda function (a small piece of code that runs in the cloud) which forwards the job to your relay server. You'll need free accounts on both the [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask) and [AWS](https://aws.amazon.com).

#### Step 1 — Create the Lambda function

1. Sign in to the [AWS Console](https://console.aws.amazon.com) and go to **Lambda**
2. Click **Create function**
3. Choose **Author from scratch**, give it a name like `VoiceLabelPrinter`, and set the runtime to **Python 3.12**
4. Click **Create function**
5. In the **Code** tab, open the file tree on the left and click `lambda_function.py`
6. Delete all the placeholder code and paste in the entire contents of `alexa-skill/lambda_function.py` from this repo
7. Click **Deploy**

#### Step 2 — Set Lambda environment variables

1. In your Lambda function, click the **Configuration** tab → **Environment variables** → **Edit**
2. Add these three variables:

   | Key | Value |
   |---|---|
   | `WEBHOOK_URL` | `https://your-relay-server.com/webhook` |
   | `SETTINGS_URL` | `https://your-relay-server.com/settings` |
   | `LABEL_TOKEN` | your secret token |

3. Click **Save**

#### Step 3 — Create the Alexa skill

1. Sign in to the [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask) and click **Create Skill**
2. Name it `Label Printer`, choose **Custom** model and **Alexa-hosted (Python)** — then switch to **Provision your own** hosting
3. On the left sidebar, click **JSON Editor**
4. Delete everything in the editor and paste in the full contents of `alexa-skill/interaction_model.json` from this repo
5. Click **Save Model**, then **Build Model** — wait for it to finish (takes about a minute)

#### Step 4 — Connect Lambda to the skill

1. In your Lambda function, click **+ Add trigger** → search for **Alexa Skills Kit**
2. Paste your **Alexa Skill ID** (found in the Alexa Developer Console under the skill name) and click **Add**
3. Copy your Lambda function's **ARN** from the top right of the Lambda page (looks like `arn:aws:lambda:us-east-1:123456789:function:VoiceLabelPrinter`)
4. Back in the Alexa Developer Console, go to **Endpoint** in the left sidebar
5. Select **AWS Lambda ARN** and paste your ARN into the **Default Region** field
6. Click **Save Endpoints**, then rebuild the model one more time

#### Step 5 — Test it

Say *"Alexa, open label printer"* — she should respond *"Label printer ready."* If she says the skill isn't responding, double-check the Lambda ARN is correct and the Skill ID trigger is set up on the Lambda side.

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
| `settings.json` | Current printer, size, font, border, style preset, saved default style, etc. |
| `history.json` | Print history (last 500) with full render settings |
| `addresses.json` | Saved address book entries |
| `config.json` | Advanced-page overrides: relay URL, token, Telegram credentials, emoji darkness |
| `custom_emojis.json` | Custom keyword → emoji mappings (with per-entry enabled flag) |
| `custom_sizes.json` | User-defined label sizes (name + dimensions + unit) |

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
├── start-all.bat          # All-local: install deps + launch server & client (Option D)
├── run-all.bat            # All-local: fast launch (no deps), used by auto-start
├── setup-windows.ps1      # All-local: firewall rules + login auto-start (one-time)
├── client/
│   ├── app.py              # Flask web UI + background polling thread + tray icon
│   ├── printer.py          # Label rendering (Pillow) + Windows GDI printing
│   ├── emoji_data.py       # 3,800+ keyword → emoji mappings (see EMOJIS.md)
│   ├── requirements.txt
│   ├── images/             # Drop custom border images here (border_<name>.png)
│   ├── static/             # favicon.ico, favicon.png
│   └── templates/
│       ├── index.html      # Single-page web UI
│       └── advanced.html   # PC-only Advanced Settings page (tabbed)
├── server/
│   ├── app.py              # Flask relay server (shared by Docker + local)
│   ├── run_local.py        # All-local Windows launcher: tray + setup page (Option D)
│   ├── start-local.bat     # Install deps + launch server only
│   ├── requirements.txt        # Docker deps (gunicorn)
│   ├── requirements-local.txt  # Local Windows deps (Flask dev server + tray)
│   ├── Dockerfile
│   └── docker-compose.yml
└── alexa-skill/
    ├── lambda_function.py  # AWS Lambda handler
    └── interaction_model.json
```

---

## Security Notes

### How it's secured
- `LABEL_TOKEN` is required on every request to the relay server — anything without it gets a `401 Unauthorized`
- The token is sent as an `X-Token` HTTP header (not in the URL, so it never appears in server access logs)
- The relay server has rate limiting on all endpoints to prevent abuse
- The server only accepts a known allowlist of setting keys and values — arbitrary data can't be injected
- `server/.env` and `client/.env` are **gitignored** — never commit them

### The client web UI is unauthenticated
The client UI (port `5000`) has **no password**. By default it binds to `0.0.0.0` so you can open it from your phone, which means anyone on the same network can reach it and print/change settings. This is a deliberate convenience tradeoff for a trusted home LAN. To lock it down:
- **Don't** port-forward `5000` to the internet (only the token-protected relay on `5001` is safe to expose, and even then prefer the cloud options).
- If you don't need phone access, you can bind the client to localhost only — change its `app.run(host="0.0.0.0", …)` to `host="127.0.0.1"`.

### Use a strong token
The token is the only thing standing between your printer and the internet. Use something long and random — not a word or phrase. A good way to generate one:

```python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

This produces something like `3Kx9mP2vL8nQ4wRjF7tYcZ1oBsHdEuAg` — use this as your `LABEL_TOKEN` in all three places (server, client, Lambda).

### The same token goes in multiple places
| Where | How |
|---|---|
| Relay server | `LABEL_TOKEN` env var (Railway/Render dashboard or `server/.env`) |
| Windows client | `LABEL_TOKEN` in `client/.env` |
| AWS Lambda | `LABEL_TOKEN` env var in Lambda configuration |
| Siri Shortcut | `X-Token` header in the **Get Contents of URL** action |

If any one of these doesn't match, that component stops working — which is a useful way to rotate the token if you ever think it's been compromised.

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
| `python-barcode` | Code 128 Barcode style preset |
| `uharfbuzz` | HarfBuzz text shaping for ZWJ emoji sequences |
| `freetype-py` | FreeType rendering of color emoji bitmaps |
| `fonttools` | PNG bitmap extraction from Noto Color Emoji (country flags + Unicode 15) |

### Server
| Package | Purpose |
|---|---|
| `flask` | HTTP API |
| `gunicorn` | WSGI production server |
