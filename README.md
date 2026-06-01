# meeting-sender

Lives on your **work laptop**. A single HTML file — no Python, no install, nothing.

Just open `index.html` in any browser and drag in a `.vtt` file.

## Setup

1. Clone or download this repo on your work laptop
2. Open `index.html` directly in Chrome/Edge/Firefox
3. Click **⚙️ Connection Settings** and enter:
   - **Receiver URL** — your desktop's local IP + port, e.g. `http://192.168.1.50:5002`
   - **Auth Token** — the same secret you put in the receiver's `.env`
4. Hit **Save** (settings are stored in the browser's localStorage)

That's it. Drag a `.vtt` file in and press **Send for Analysis**.

## Finding your desktop's IP

On your main computer, run `ipconfig` and look for your WiFi or Ethernet IPv4 address (usually `192.168.x.x`).

## Flow

```
index.html (browser)
  └─ POST /upload  ──→  meeting-receiver (main computer)
                           └─ Hermes /analyze-meeting
                               └─ 17-section report → Dashboard
```
