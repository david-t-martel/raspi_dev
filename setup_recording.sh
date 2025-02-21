#!/bin/bash

echo "🎥 Setting up FFmpeg recording and HLS re-streaming..."

cat << EOF | sudo tee /usr/local/bin/start_recording.sh
#!/bin/bash
ffmpeg -i rtsp://127.0.0.1:8554/stream -c copy -t 3600 /var/www/html/output.mp4 &
ffmpeg -i rtsp://127.0.0.1:8554/stream \
-c:v copy -hls_time 5 -hls_list_size 10 -hls_flags delete_segments \
-f hls /var/www/html/live.m3u8
EOF

sudo chmod +x /usr/local/bin/start_recording.sh

echo "✅ Recording and HLS setup complete."
