# matrixpi

matrixpi repository for Avans VSR assignment.

## Documentation

- **[Documentation/README.md](Documentation/README.md)** — full documentation index.
- **[Documentation/GettingStarted.md](Documentation/GettingStarted.md)** — run the app on your own laptop in 5 minutes (no Raspberry Pi needed). **Start here if you're new.**
- **[Documentation/Overview.md](Documentation/Overview.md)** — what the project is and how the pieces fit together.
- **[Documentation/HowTo.md](Documentation/HowTo.md)** — cookbook for common changes (add a page, translation, setting, etc.).

## Usage

### Setup

See [SETUP.md](Documentation/SETUP.md) on how to set up matrixpi

### Optional: Setting up the SoftAP

To be able to connect to the RPI without an external router, your can configure the RPI as a SoftAP. See [SOFTAP.md](Documentation/SOFTAP.md).

### Optional: Start matrixpi on boot

To start matrixpi on boot, you can enable it as a systemd service. See [SYSTEMD.md](Documentation/SYSTEMD.md).

### Starting the program

This program needs to be run with sudo. This is because we need sudo to control GPIO 18.

```
# Navigate to the matrixpi root directory
cd ~/matrixpi

# Activate the virtualenv (if not done already)
source .venv/bin/activate

# Start the program (WITH SUDO)
sudo .venv/bin/python server.py
```

#### Docker

For docker usage see [DOCKER.md](Documentation/DOCKER.md).

## Hardware

For a schematic and physical layout of the hardware, see [HardwareMatrix.md](Documentation/HardwareMatrix.md).

## Software

For a list of used libraries and technologies, see [SOFTWARE.md](Documentation/SOFTWARE.md).