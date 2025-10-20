import os

def clear_downloads():
    downloads = './downloads'

    if not os.path.exists(downloads):
        print("⚠️ Downloads folder does not exist.")
        return

    files = os.listdir(downloads)
    if not files:
        print("ℹ️ Downloads folder is already empty.")
        return

    for file in files:
        file_path = os.path.join(downloads, file)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
                print(f"✅ Removed file: {file}")
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
                print(f"✅ Removed folder: {file}")
        except Exception as e:
            print(f"❌ Failed to remove {file}: {e}")

    print(f"\n✅ Cleared all downloads from {downloads}")

# Example usage
if __name__ == "__main__":
    clear_downloads()
