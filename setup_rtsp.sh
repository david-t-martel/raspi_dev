#!/bin/bash

echo "🔧 Configuring RTSP streaming service..."

# Load credentials
export $(grep -v '^#' .env | xargs)

cat << EOF | sudo tee /usr/local/bin/start_rtsp.sh
#!/bin/bash
gst-launch-1.0 rpicamsrc preview=false \
! video/x-h264, width=1280, height=720, framerate=30/1 \
! h264parse \
! rtspclientsink location=rtsp://\$RTSP_USER:\$RTSP_PASS@127.0.0.1:8554/stream
EOF

sudo chmod +x /usr/local/bin/start_rtsp.sh
echo "✅ RTSP setup complete with secure authentication."
