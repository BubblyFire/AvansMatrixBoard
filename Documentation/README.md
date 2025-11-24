# Raspberry Pi Setup

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

### Step 3: Setting up the SoftAP

```
# Navigate to the matrixpi root directory
cd ~/matrixpi

# Run the AP installer
cd tools/ap && sudo ./installconfig.sh && cd ../..

# Select 1 and press enter to install
# Wait for the installation to finish
# Select 9 and press enter to exit
```

The default SSID and password are 'matrixpi' and 'matrixpiavans' respectively.

Once the SoftAP is set-up, the RPI will get 192.168.50.5 by default.

### Step 4: Setting up the Python virtualenv

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

## Starting the program

### Option A: Python virtualenv

This program needs to be run with sudo. This is because we need sudo to control GPIO 18.

```
# Navigate to the matrixpi root directory
cd ~/matrixpi

# Activate the virtualenv (if not done already)
source .venv/bin/activate

# Start the program (WITH SUDO)
sudo .venv/bin/python server.py
```

### Option B: Docker container

> **WARNING** Currently not working

```
# Build the docker container image
docker build -t matrixpi-image .

# Run the container
docker run -p 5000:5000 --name my-matrixpi-container matrixpi-image
```
