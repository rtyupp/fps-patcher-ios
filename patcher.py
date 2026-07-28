import struct
import os
import sys

def list_files(directory):
    """List MP4 files with numbers for selection"""
    try:
        files = [f for f in os.listdir(directory) if f.lower().endswith('.mp4')]
        return files
    except:
        return []

def pick_file_interactive():
    """Interactive file picker that works in a-Shell"""
    # First check current directory
    current_files = list_files(".")
    
    print("\n📂 Looking for MP4 files...")
    print("="*45)
    print("Press 1️⃣  to browse current folder")
    print("Press 2️⃣  to browse Documents folder")
    print("Press 3️⃣  to enter full path manually")
    print("="*45)
    
    choice = input("Your choice: ").strip()
    
    search_dir = "."
    if choice == "2":
        search_dir = "~/Documents"
    elif choice == "3":
        path = input("📂 Enter full path to MP4 file: ").strip()
        if os.path.exists(path) and path.lower().endswith('.mp4'):
            return path
        else:
            print("❌ Invalid file!")
            return None
    
    files = list_files(search_dir)
    
    if not files:
        print(f"❌ No MP4 files found in {search_dir}")
        print("💡 Tip: Move your video to this folder first:")
        print(f"   {search_dir}")
        return None
    
    print(f"\n📁 Found {len(files)} MP4 file(s):")
    print("-"*40)
    for i, f in enumerate(files, 1):
        size = os.path.getsize(os.path.join(search_dir, f))
        size_mb = size / (1024 * 1024)
        print(f"  {i}. {f} ({size_mb:.1f} MB)")
    print("-"*40)
    
    while True:
        try:
            num = int(input("Select number (or 0 to cancel): "))
            if num == 0:
                return None
            if 1 <= num <= len(files):
                selected = os.path.join(search_dir, files[num-1])
                print(f"✅ Selected: {files[num-1]}")
                return selected
            else:
                print(f"❌ Choose between 1 and {len(files)}")
        except ValueError:
            print("❌ Enter a number!")

def get_fps():
    """Ask for original FPS"""
    print("\n🎯 Common FPS values: 24, 30, 60, 120")
    while True:
        fps_input = input("Enter original FPS of your video: ").strip()
        try:
            fps = float(fps_input)
            if fps > 0:
                return fps
            else:
                print("❌ Must be positive!")
        except ValueError:
            print("❌ Enter a valid number!")

def patch_video_fps(input_path, original_fps, target_fps=30.0):
    """Patch MP4 metadata to change FPS without re-encoding"""
    print(f"\n⏳ Reading: {os.path.basename(input_path)}")
    
    try:
        with open(input_path, 'rb') as f:
            data = bytearray(f.read())
    except Exception as e:
        print(f"❌ Cannot read file: {e}")
        return None

    scale = original_fps / target_fps
    patched_count = 0
    pos = 0
    file_size = len(data)
    
    print("🔧 Scanning for metadata atoms...")
    
    while pos < file_size - 8:
        # Patch mvhd atom
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

        # Patch mdhd atom
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
        print("❌ Could not find metadata atoms. Is this a valid MP4?")
        return None

    # Generate output filename
    dir_name = os.path.dirname(input_path) or "."
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(dir_name, f"{base_name}_30fps.mp4")

    print(f"💾 Saving: {os.path.basename(output_path)}")
    
    try:
        with open(output_path, 'wb') as f:
            f.write(data)
    except Exception as e:
        print(f"❌ Cannot write file: {e}")
        return None

    print(f"✅ Patched {patched_count} atoms successfully!")
    print(f"📁 Saved: {os.path.basename(output_path)}")
    return output_path

def main():
    print("\n" + "="*45)
    print("   🎬 FPS Patcher for TikTok")
    print("   Metadata Patcher - No Re-encode")
    print("="*45)
    
    # Step 1: Select file
    file_path = pick_file_interactive()
    
    if not file_path:
        print("\n👋 Goodbye!")
        return
    
    # Step 2: Get FPS
    original_fps = get_fps()
    
    # Step 3: Patch
    print("\n" + "="*45)
    print(f"⚡ Converting {original_fps}fps → 30fps")
    print("="*45)
    
    result = patch_video_fps(file_path, original_fps, 30.0)
    
    if result:
        print("\n" + "="*45)
        print("🎉 SUCCESS!")
        print("📤 Upload the _30fps.mp4 file to TikTok")
        print("="*45)
    else:
        print("\n❌ Patching failed. Check your file.")

if __name__ == "__main__":
    main()
