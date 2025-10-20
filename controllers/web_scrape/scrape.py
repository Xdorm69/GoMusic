import yt_dlp
import pandas as pd
import re


def clean_title(title: str):
    # Split by common separators or unwanted keywords
    parts = re.split(r'\s*(?:\||-|:|\(|\b(?:song|intro|album|new)\b)\s*', title, flags=re.IGNORECASE)
    clean = parts[0].strip()
    return clean


def search_youtube_songs(artist_name, language):
    query = f"{artist_name} {language} songs"
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,  # only metadata, no video download
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch15:{query}", download=False)

    videos = []
    seen_titles = set()  # track lowercase titles to avoid duplicates

    for entry in info['entries']:
        title = entry.get('title')
        if not title:
            continue

        clean = clean_title(title)
        if('best of' in clean.lower() or 'top' in clean.lower()):
            continue

        # Skip if in exclude list
        if clean.lower() in seen_titles:
            continue

        seen_titles.add(clean.lower())

        videos.append({
            'artist': artist_name,
            'language': language,
            'title': clean,
        })
        print(f"🎵 {clean}")

    # Save to CSV
    df = pd.DataFrame(videos)
    df.to_csv("youtube_songs.csv", index=False)
    print(f"\n✅ Saved {len(df)} songs to youtube_songs.csv")

if __name__ == "__main__":
    search_youtube_songs("dhanda nyoliwala", "haryanvi")
