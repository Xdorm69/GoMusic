import os
import shutil

def copy_downloads():
    downloads = './downloads'
    destination = './data'

    # Ensure destination exists
    os.makedirs(destination, exist_ok=True)

    # List all mp3 files in downloads
    songs = [f for f in os.listdir(downloads) if f.endswith(".mp3")]

    if not songs:
        print("⚠️ No mp3 files found in downloads.")
        return

    # Copy each file
    for song in songs:
        src_path = os.path.join(downloads, song)
        dest_path = os.path.join(destination, song)
        shutil.copy2(src_path, dest_path)  # copy2 preserves metadata
        print(f"✅ Copied: {song}")

    print(f"\n✅ All {len(songs)} songs copied to {destination}")

# Example usage
if __name__ == "__main__":
    copy_downloads()
