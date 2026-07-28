#!/bin/sh

echo ""
echo "========================================="
echo "  🎬 FPS Patcher - FFmpeg Edition"
echo "  For TikTok Smooth Playback"
echo "========================================="
echo ""

# Step 1: List MP4 files
echo "📂 Looking for MP4 files..."
echo ""

count=0
for f in *.mp4; do
    [ -e "$f" ] || continue
    count=$((count + 1))
    size=$(du -h "$f" | cut -f1)
    echo "  $count. $f ($size)"
done

if [ $count -eq 0 ]; then
    echo "❌ No MP4 files found!"
    echo "💡 Move your video to this folder first"
    exit 1
fi

echo ""
echo "Press number to select, or 0 to cancel:"
read num

if [ "$num" = "0" ] || [ -z "$num" ]; then
    echo "👋 Goodbye!"
    exit 0
fi

# Get selected file
selected=""
count=0
for f in *.mp4; do
    [ -e "$f" ] || continue
    count=$((count + 1))
    if [ "$count" = "$num" ]; then
        selected="$f"
        break
    fi
done

if [ -z "$selected" ]; then
    echo "❌ Invalid selection!"
    exit 1
fi

echo ""
echo "✅ Selected: $selected"
echo ""
echo "Choose mode:"
echo "  1. Same speed (recommended for TikTok)"
echo "  2. Keep all frames (slow motion)"
echo ""
read mode

# Get base name
base="${selected%.*}"

if [ "$mode" = "2" ]; then
    # Keep all frames = slow motion
    output="${base}_30fps_slow.mp4"
    echo ""
    echo "⚡ Converting to 30fps (keep all frames)..."
    ffmpeg -i "$selected" -c copy -bsf:v h264_metadata=fixed_fps=30 \
           -fps_mode passthrough "$output" -y 2>/dev/null
else
    # Same speed = drop every 2nd frame evenly
    output="${base}_30fps_fast.mp4"
    echo ""
    echo "⚡ Converting to 30fps (same speed)..."
    ffmpeg -i "$selected" -filter:v "fps=30" -c:a copy "$output" -y 2>/dev/null
fi

if [ -f "$output" ]; then
    size=$(du -h "$output" | cut -f1)
    echo ""
    echo "========================================="
    echo "  🎉 SUCCESS!"
    echo "  📁 Saved: $output ($size)"
    echo "  📤 Upload this to TikTok"
    echo "========================================="
else
    echo ""
    echo "❌ Conversion failed!"
fi
