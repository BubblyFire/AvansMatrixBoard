# matrixpi

matrixpi repository for Avans VSR assignment.

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

> **WARNING** Currently not working

## Hardware

For a schematic and physical layout of the hardware, see [HARDWARE.md](Documentation/HARDWARE.md).

## Software

For a list of used libraries and technologies, see [SOFTWARE.md](Documentation/SOFTWARE.md).