# systemd setup

systemd can be used to automatically start the MatrixPi application as a service on boot.

```
# Navigate to the repo directory
cd ~/matrixpi

# Copy the file
cp tools/systemd/matrixpi.service /etc/systemd/system/

# Reload systemd
sudo systemctl daemon-reload

# Enable the service
sudo systemctl enable matrixpi

# Start the service
sudo systemctl start matrixpi
```

You can view the status of MatrixPi with:
```
sudo systemctl status matrixpi
```

> **NOTE** Check matrixpi.service and verify that `WorkingDirectory` and `ExecStart` are set correctly.
