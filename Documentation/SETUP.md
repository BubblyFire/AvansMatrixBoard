# matrixpi setup

This is the setup guide for installing the matrixpi software to a clean Raspberry Pi 4 Model B.

## Flash the RPI OS to the SD card

### Step 1: Download RPI imager

Download *RPI Imager v1.8.5* for [Windows](https://downloads.raspberrypi.org/imager/imager_1.8.5.exe), [Linux](https://downloads.raspberrypi.org/imager/imager_1.8.5_amd64.deb), or [MacOS](https://downloads.raspberrypi.org/imager/imager_1.8.5.dmg).

### Step 2: Select the OS

Select *Raspberry PI OS Lite (64-bit) 2024-03-15*. If this is not available anymore, [download it manually](https://downloads.raspberrypi.com/raspios_lite_arm64/images/raspios_lite_arm64-2024-03-15/) and select it in the imager.

### Step 3: OS customization

Go to OS customization and set the following options:

| Setting | Value |
|---|---|
| Hostname | matrixpi |
| Username | avans |
| Password | avans |
| Timezone | Europe/Amsterdam |
| Enable SSH | Use password authentication |

### Step 4: Flash

Flash to the SD card.

## Initial boot

Make sure that you can access the RPI via SSH or directly with a keyboard and display.
You can access the RPI via the IP given to it by your router, or its hostname: *matrixpi*.

### Step 1: Update and install software

When installing everything the first time, the RPI has to be connected to the internet.

```
# Update the system
sudo apt update && sudo apt upgrade -y

# Install all required dependencies
sudo apt install git python3 python3-pip git -y

# Navigate to the home directory
cd ~

# Clone the repository
git clone https://github.com/telintelo/matrixpi.git
```

### Step 2: Disabling GPIO 18 audio PCM clock

GPIO 18 will be used as the NeoPixel data pin. It has fast direct memory access and is therefore useful for driving devices that require very specific timing.
GPIO 18 is by default used as a PCM clock signal for external audio devices.
To disable the PCM clock for this pin, disable audio in the boot config.txt with the following command:

```
sudo sed -i 's/dtparam=audio=on/dtparam=audio=off/g' /boot/firmware/config.txt
```

### Step 3: Setting up the Python virtualenv

```
# Navigate to the matrixpi root directory
cd ~/matrixpi

# Create the virtualenv
python3 -m venv .venv

# Activate the virtualenv
source .venv/bin/activate

# Install the dependencies
pip install -r requirements.txt
```

### Step 4: Start the program

The program needs `sudo` because it drives GPIO 18.

```
# From ~/matrixpi with the virtualenv active
sudo .venv/bin/python server.py
```

You should see Flask startup output ending with something like:

```
 * Running on http://0.0.0.0:80
```

### Step 5: Verify it works

On another device connected to the same network, open:

```
http://matrixpi/
```

Or, if the hostname doesn't resolve, use the Pi's IP address (e.g. `http://192.168.1.42/`). You can find it with `hostname -I` on the Pi.

You should see the home page. Try the **Text** page — typing a message and clicking send should light up the matrix.

### Troubleshooting

| Problem | Fix |
|---|---|
| `Permission denied` on GPIO | You forgot `sudo`. The program needs it for GPIO 18. |
| `Address already in use` on port 80 | Something else is using port 80. `sudo lsof -i :80` shows what. |
| The web page loads but the matrix stays dark | Check wiring (see [HardwareMatrix.md](HardwareMatrix.md)), the `pin` setting on `/config`, and that audio is disabled (Step 2). |
| `hostname: matrixpi` doesn't resolve | Use the IP address from `hostname -I`. On Windows, `.local` resolution sometimes requires Bonjour. |
| `ModuleNotFoundError: No module named 'board'` | `rpi_ws281x` / `Adafruit-Blinka` didn't install. Re-run `pip install -r requirements.txt` inside the virtualenv. |

### Optional next steps

- **Access the Pi without a router** — set up the SoftAP: [SOFTAP.md](SOFTAP.md).
- **Auto-start matrixpi on boot** — [SYSTEMD.md](SYSTEMD.md).
- **Change hardware or image-processing settings** — open `/config` in the browser, or read [Config.md](Config.md).