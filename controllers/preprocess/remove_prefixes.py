import os
import pandas as pd

def remove_prefixes(path='./data'):
    os.makedirs(path, exist_ok=True)
    songs = [file for file in os.listdir(path) if file.endswith(".mp3")]

    if not songs:
        print("No MP3 files found in the folder.")
        return []

    print("\nFound songs with prefixes:")
    prefixes = []
    
    for i, song in enumerate(songs, start=1):
        if(song.split(" ")[0].isdigit() and len(song.split(" ")) > 1):
            print(f"{i}. {song}")
            prefixes.append(song)
        elif (song.split("_")[0].isdigit() and len(song.split("_")) > 1):
            print(f"{i}. {song}")
            prefixes.append(song)

    q = input("\nEnter 'y' to confirm removing numeric prefixes: ").strip().lower()
    if q != 'y':
        print("No prefixes removed 🤷")
        return []

    prefixes_removed_data = []

    for song in prefixes:
        original_path = os.path.join(path, song)
        new_name = song

        # Handle prefixes separated by space or underscore
        parts_space = song.split(" ", 1)
        parts_underscore = song.split("_", 1)

        if parts_space[0].isdigit() and len(parts_space) > 1:
            new_name = parts_space[1]
        elif parts_underscore[0].isdigit() and len(parts_underscore) > 1:
            new_name = parts_underscore[1]

        # Skip if no change
        if new_name == song:
            continue

        new_path = os.path.join(path, new_name)

        # Handle duplicates safely
        if os.path.exists(new_path):
            base, ext = os.path.splitext(new_name)
            new_name = f"{base}_renamed{ext}"
            new_path = os.path.join(path, new_name)

        os.rename(original_path, new_path)
        prefixes_removed_data.append({"old_name": song, "new_name": new_name})

    # Save report to CSV
    if prefixes_removed_data:
        pd.DataFrame(prefixes_removed_data).to_csv(
            os.path.join(path, 'prefixes_removed_data.csv'),
            index=False
        )
        print(f"\n✅ Prefixes removed and saved report to '{path}/prefixes_removed_data.csv'")
    else:
        print("No prefixes found to remove.")

    return prefixes_removed_data

if __name__ == "__main__":
    remove_prefixes()
