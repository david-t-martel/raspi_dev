#!/bin/bash

echo "🔄 Updating system..."
sudo apt update && sudo apt upgrade -y

echo "✅ Installing dependencies..."
sudo apt install -y git cmake gstreamer1.0-tools gstreamer1.0-rtsp gstreamer1.0-libav \
                    gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly \
                    ffmpeg nginx curl cron python3-flask python3-dotenv

echo "🔐 Creating .env file for secure credentials..."
if [ ! -f .env ]; then
    cat <<EOF > .env
RTSP_USER=admin
RTSP_PASS=securepassword
WEB_USERNAME=admin
WEB_PASSWORD=websecurepassword
FLASK_SECRET_KEY=myflasksecret
RTSP_PORT=8554
EOF
fi

echo "🔧 Configuring GPU acceleration..."
if ! grep -q "^gpu_mem=" /boot/config.txt; then
    echo "gpu_mem=128" | sudo tee -a /boot/config.txt
else
    sudo sed -i 's/^gpu_mem=.*/gpu_mem=128/' /boot/config.txt
fi


echo "📁 Setting up scheduled cleanup for recordings..."
(crontab -l 2>/dev/null; echo "0 3 * * * find /var/www/html/ -type f -name '*.mp4' -mtime +3 -delete") | crontab -

echo "🚀 Installing RTSP, ONVIF, and Recording services..."
./setup_rtsp.sh
./setup_onvif.sh
./setup_recording.sh

echo "📊 Setting up Dashboard Web UI..."
sudo cp systemd/dashboard.service /etc/systemd/system/
sudo systemctl enable dashboard.service
sudo systemctl start dashboard.service

echo "✅ Installation complete! Camera and dashboard are now running."
