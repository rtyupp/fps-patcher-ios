#!/bin/sh

echo ""
echo "========================================="
echo "  🎬 FPS Patcher - FFmpeg Edition"
echo "  For TikTok Smooth Playback"
echo "========================================="
echo ""

# فتح متصفح الملفات مباشرة
echo "📂 Opening file picker..."
echo "   (Browse to your video and select it)"
echo ""

video=$(pickfile)

if [ -z "$video" ]; then
    echo "❌ No file selected."
    echo "👋 Goodbye!"
    exit 1
fi

echo ""
echo "✅ Selected: $(basename "$video")"
echo ""
echo "Choose mode:"
echo "  1. Same speed (recommended for TikTok)"
echo "  2. Keep all frames (slow motion)"
echo ""
read -p "Your choice (1 or 2): " mode

base="${video%.*}"

if [ "$mode" = "2" ]; then
    # Keep all frames = slow motion
    output="${base}_30fps_slow.mp4"
    echo ""
    echo "⚡ Converting to 30fps (keep all frames)..."
    ffmpeg -i "$video" -c copy -bsf:v h264_metadata=fixed_fps=30 \
           -fps_mode passthrough "$output" -y 2>/dev/null
else
    # Same speed
    output="${base}_30fps_fast.mp4"
    echo ""
    echo "⚡ Converting to 30fps (same speed)..."
    ffmpeg -i "$video" -filter:v "fps=30" -c:a copy "$output" -y 2>/dev/null
fi

if [ -f "$output" ]; then
    echo ""
    echo "========================================="
    echo "  🎉 SUCCESS!"
    echo "  📁 Saved: $(basename "$output")"
    echo "  📤 Upload this file to TikTok"
    echo "========================================="
else
    echo ""
    echo "❌ Conversion failed. Check your video file."
fi
