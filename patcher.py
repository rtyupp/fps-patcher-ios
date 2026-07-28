import struct
import os
import sys
import subprocess

def pick_file():
    """Use a-Shell's pickfile to select a video"""
    print("📂 Opening file picker...")
    try:
        result = subprocess.run(["pickfile"], capture_output=True, text=True, timeout=120)
        if result.returncode == 0 and result.stdout.strip():
            filepath = result.stdout.strip()
            print(f"✅ Selected: {os.path.basename(filepath)}")
            return filepath
        else:
            print("❌ No file selected or pickfile failed.")
            return None
    except FileNotFoundError:
        print("❌ 'pickfile' command not available.")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def get_fps():
    """Ask user for original FPS"""
    while True:
        fps_input = input("🎯 Enter original FPS (e.g., 60): ").strip()
        try:
            fps = float(fps_input)
            if fps > 0:
                return fps
            else:
                print("❌ Must be a positive number!")
        except ValueError:
            print("❌ Please enter a valid number!")

def patch_video_fps(input_path, original_fps, target_fps=30.0):
    """Patch MP4 metadata to change FPS"""
    if original_fps <= 0 or target_fps <= 0:
        print("❌ Error: FPS values must be positive numbers.")
        return None

    if not input_path.lower().endswith('.mp4'):
        print("❌ Error: File must be an MP4.")
        return None

    print(f"⏳ Reading file: {os.path.basename(input_path)}")
    try:
        with open(input_path, 'rb') as f:
            data = bytearray(f.read())
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None

    scale = original_fps / target_fps
    patched_count = 0
    pos = 0
    file_size = len(data)

    print("🔧 Patching metadata atoms...")
    while pos < file_size - 8:
        if data[pos:pos+4] == b'mvhd':
            if pos + 20 <= file_size:
                timescale = struct.unpack('>I', data[pos+16:pos+20])[0]
                duration = struct.unpack('>I', data[pos+20:pos+24])[0]
                
                new_timescale = int(timescale / scale)
                new_duration = int(duration / scale)
                
                data[pos+16:pos+20] = struct.pack('>I', new_timescale)
                data[pos+20:pos+24] = struct.pack('>I', new_duration)
                
                patched_count += 1
                pos += 20
                continue

        elif data[pos:pos+4] == b'mdhd':
            if pos + 20 <= file_size:
                timescale = struct.unpack('>I', data[pos+16:pos+20])[0]
                duration = struct.unpack('>I', data[pos+20:pos+24])[0]
                
                new_timescale = int(timescale / scale)
                new_duration = int(duration / scale)
                
                data[pos+16:pos+20] = struct.pack('>I', new_timescale)
                data[pos+20:pos+24] = struct.pack('>I', new_duration)
                
                patched_count += 1
                pos += 20
                continue

        pos += 1

    if patched_count == 0:
        print("❌ Error: Could not find mvhd or mdhd atoms in the MP4 file.")
        return None

    # Create output filename
    dir_name = os.path.dirname(input_path)
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(dir_name, f"{base_name}_30fps.mp4")

    print("💾 Saving patched file...")
    try:
        with open(output_path, 'wb') as f:
            f.write(data)
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return None

    print(f"✅ Success! Patched {patched_count} atoms.")
    print(f"📁 Saved to: {os.path.basename(output_path)}")
    return output_path

def main():
    print("\n" + "="*45)
    print("   🎬 FPS Metadata Patcher for TikTok")
    print("   a-Shell Edition - Auto File Picker")
    print("="*45)
    
    # Automatically open file picker
    file_path = pick_file()
    
    if not file_path:
        print("\n❌ Operation cancelled. Run again to select a file.")
        return
    
    # Get original FPS
    original_fps = get_fps()
    
    # Start patching
    print(f"\n⚡ Patching from {original_fps}fps to 30fps...")
    print("-"*45)
    
    result = patch_video_fps(file_path, original_fps, 30.0)
    
    if result:
        print("-"*45)
        print("🎉 Done! Upload this new file to TikTok.")
        print("   It will play smoothly at 30fps.")
    else:
        print("-"*45)
        print("❌ Patching failed. Try a different MP4 file.")

if __name__ == "__main__":
    main()
