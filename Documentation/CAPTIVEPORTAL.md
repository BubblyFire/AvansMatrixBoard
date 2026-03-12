# Captive Portal Setup

When a phone or laptop connects to the `matrixpi` WiFi network, a captive portal
automatically opens the matrix board web interface in the browser — no need to
manually type an IP address.

## How it works

When a device connects to a WiFi network it immediately checks for internet access
by visiting a known URL (different per operating system). If the response is not
what it expects, the OS shows a **"Sign in to network"** popup and opens a browser.

We make use of this by:
1. Redirecting all DNS queries to the Pi's own IP address
2. Adding routes to Flask that respond to the OS connectivity checks

---

## Prerequisites

The SoftAP must already be set up before doing any of the steps below.
See [SOFTAP.md](SOFTAP.md) if you haven't done this yet.

After the SoftAP setup the Pi's IP address on the WiFi network is `192.168.50.5`.

---

## Step 1 — Redirect all DNS to the Pi

`dnsmasq` is the DNS and DHCP server installed by the SoftAP setup.
It needs one extra line to resolve every domain name to the Pi's IP address.
This is what triggers the captive portal detection on phones.

Open the dnsmasq config file:

```bash
sudo nano /etc/dnsmasq.conf
```

Add this line at the bottom:

```
address=/#/192.168.50.5
```

Save the file and restart dnsmasq:

```bash
sudo systemctl restart dnsmasq
```

> **What this does:** any domain a connected device looks up (e.g. `google.com`,
> `captive.apple.com`) will resolve to `192.168.50.5` instead of the real address.
> The device detects there is no real internet and shows the captive portal popup.

---

## Step 2 — Add captive portal routes to Flask

Each operating system checks a different URL to detect captive portals.
Flask needs to respond to these URLs so the browser redirect happens automatically.

Create a new file `app/routes/pages/routes/portal.py`:

```python
from flask import redirect
from ..blueprint import core_bp

PORTAL_REDIRECT = 'http://192.168.50.5/'

# iOS and macOS check this URL
@core_bp.route('/hotspot-detect.html')
def portal_ios():
    return redirect(PORTAL_REDIRECT)

# Android and Chrome check this URL
@core_bp.route('/generate_204')
def portal_android():
    return redirect(PORTAL_REDIRECT)

# Windows checks this URL
@core_bp.route('/ncsi.txt')
def portal_windows():
    return redirect(PORTAL_REDIRECT)
```

Then register it in `app/routes/pages/__init__.py` by adding `portal` to the imports:

```python
from .routes import home, draw, text, image_uploads, imagepicker, pi_files, status, slideshow, portal
```

Restart the Flask app for the changes to take effect.

---

## Step 3 — Test it

1. On your phone, disconnect from your normal WiFi
2. Connect to the `matrixpi` network (password: `matrixpiavans`)
3. A **"Sign in to network"** notification should appear within a few seconds
4. Tap it — the browser should open directly to the matrix board interface

If the popup does not appear, open a browser manually and go to `http://192.168.50.5`.

---

## Troubleshooting

**Popup appears but the page does not load**
Make sure the Flask app is running with `sudo` on the Pi:
```bash
sudo .venv/bin/python server.py
```

**No popup appears at all**
- Check that dnsmasq is running: `sudo systemctl status dnsmasq`
- Check that the `address=/#/192.168.50.5` line was saved correctly
- Some devices take up to 30 seconds to detect the captive portal

**Works on iPhone but not Android (or vice versa)**
Make sure all three routes (`/hotspot-detect.html`, `/generate_204`, `/ncsi.txt`)
are registered in Flask and the app has been restarted.

**Connected devices lose internet access**
This is expected — the DNS redirect means all traffic stays on the Pi.
The captive portal is only meant for local use without an internet connection.
