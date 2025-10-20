import pandas as pd

# Load the artist CSV once globally
artists_df = pd.read_csv('./constants/artists.csv')

# Custom short-name or nickname mapping
custom_artist_names = {
    "aujla": "Karan Aujla",
    "prem": "Prem Dhillon",
    "sidhu": "Sidhu Moosewala",
    "nseeb": "Nseeb",
}

# Build a lowercase lookup dict for fast language lookup
artist_to_lang = dict(zip(artists_df['artist'].str.lower(), artists_df['language']))

def get_artist(song_title):
    title = song_title.lower()

    # Check for custom name matches first
    for key, val in custom_artist_names.items():
        if key in title:
            return val

    # Then check regular artists list
    matches = artists_df[artists_df['artist'].str.lower().apply(lambda a: a in title)]
    return matches['artist'].iloc[0] if not matches.empty else None


def get_language(artist_name):
    if not artist_name:
        return None
    return artist_to_lang.get(artist_name.lower())


def merged_data(songs_list):
    df = pd.DataFrame(songs_list, columns=['title'])

    # Apply functions
    df['artist'] = df['title'].apply(get_artist)
    df['language'] = df['artist'].apply(get_language)

    # Summary stats
    return df

