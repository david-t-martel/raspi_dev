#!/bin/bash

echo "Installing ONVIF service..."

git clone https://github.com/andvikt/onvif_srvd.git
cd onvif_srvd
mkdir build && cd build
cmake ..
make
sudo make install

echo "Configuring ONVIF service..."
sudo tee /etc/onvif_srvd.conf > /dev/null <<EOF
device_name = "RaspberryPi Camera"
manufacturer = "RaspberryPi"
model = "Zero2W"
firmware_version = "1.0"
hardware_id = "0001"
serial_number = "0001"
rtsp_port = 8554
EOF

cd ..
rm -rf onvif_srvd
echo "ONVIF setup complete."
