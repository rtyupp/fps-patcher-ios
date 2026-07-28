import struct
import os
import sys

def patch_video_fps(input_path, original_fps, target_fps=30.0):
    if original_fps <= 0 or target_fps <= 0:
        print("❌ Error: FPS values must be positive numbers.")
        return None

    if not input_path.lower().endswith('.mp4'):
        print("❌ Error: File must be an MP4.")
        return None

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

    dir_name = os.path.dirname(input_path)
    base_name = os.path.splitext(os.path.basename(input_path))[0]
    output_path = os.path.join(dir_name, f"{base_name}_{int(target_fps)}fps.mp4")

    try:
        with open(output_path, 'wb') as f:
            f.write(data)
    except Exception as e:
        print(f"❌ Error writing file: {e}")
        return None

    print(f"✅ Success! Patched {patched_count} atoms.")
    print(f"📁 Saved to: {output_path}")
    return output_path

def main_menu():
    while True:
        print("\n" + "="*50)
        print("       FPS Metadata Patcher - Terminal Edition")
        print("="*50)
        print("1️⃣  Browse & Select MP4 File")
        print("2️⃣  Set Original FPS & Patch to 30fps")
        print("0️⃣  Exit")
        print("-"*50)
        choice = input("Press number and Enter: ").strip()

        if choice == "1":
            path = input("📂 Enter full path to MP4 file: ").strip()
            if os.path.exists(path):
                print(f"✅ Selected: {path}")
                return path
            else:
                print("❌ File not found!")
                continue

        elif choice == "2":
            print("Use option 1 first to select a file!")
            continue

        elif choice == "0":
            print("👋 Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid option!")

def main():
    file_path = None
    
    # First run - immediately ask for file
    print("\n🎬 FPS Patcher for TikTok")
    print("="*40)
    print("Press 1️⃣  to select MP4 file")
    print("Press 0️⃣  to exit")
    
    first_choice = input("\nYour choice: ").strip()
    
    if first_choice == "0":
        print("👋 Goodbye!")
        return
    
    if first_choice == "1":
        path = input("📂 Enter full path to MP4 file: ").strip()
        if os.path.exists(path) and path.lower().endswith('.mp4'):
            file_path = path
            print(f"✅ Selected: {os.path.basename(path)}")
        else:
            print("❌ Invalid MP4 file!")
            return
    else:
        print("❌ Please press 1 to select a file!")
        return

    # Ask for FPS
    while True:
        fps_input = input("\n🎯 Enter original FPS (e.g., 60): ").strip()
        try:
            original_fps = float(fps_input)
            if original_fps > 0:
                break
            else:
                print("❌ Must be positive number!")
        except ValueError:
            print("❌ Please enter a number!")

    print(f"\n⏳ Patching {os.path.basename(file_path)} from {original_fps}fps to 30fps...")
    result = patch_video_fps(file_path, original_fps, 30.0)
    
    if result:
        print("\n🎉 Done! Upload this file to TikTok.")
    else:
        print("\n❌ Patching failed. Check your file and FPS value.")

if __name__ == "__main__":
    main()
