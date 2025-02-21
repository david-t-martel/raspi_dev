#!/bin/bash

echo "🎥 Setting up FFmpeg recording and HLS re-streaming..."

# Load credentials
export $(grep -v '^#' .env | xargs)

cat << EOF | sudo tee /usr/local/bin/start_recording.sh
#!/bin/bash
ffmpeg -i rtsp://\$RTSP_USER:\$RTSP_PASS@127.0.0.1:\$RTSP_PORT/stream -c copy -t 3600 /var/www/html/output.mp4 &
ffmpeg -i rtsp://\$RTSP_USER:\$RTSP_PASS@127.0.0.1:\$RTSP_PORT/stream \
-c:v copy -hls_time 5 -hls_list_size 10 -hls_flags delete_segments \
-f hls /var/www/html/live.m3u8
EOF

sudo chmod +x /usr/local/bin/start_recording.sh
echo "✅ Recording and HLS setup complete."
