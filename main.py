from re import L
from controllers.download.clear_downloads import clear_downloads
from controllers.download.copy_downloads import copy_downloads
from controllers.download.download import download_songs
from controllers.preprocess.remove_prefixes import remove_prefixes
from controllers.view.stats import stats
from controllers.view.songs import songs
from controllers.web_scrape.scrape import search_youtube_songs
from services.logger import logger
from services.ui import console, show_table

import pandas as pd

artists = pd.read_csv('./constants/artists.csv')

def print_dict(dic, title="Statistics"):
    rows = [[k, v] for k, v in dic.items()]
    show_table(
        title=title,
        columns=["Key", "Value"],
        rows=rows
    )
    logger.info(f"Displayed dictionary with {len(dic)} entries")

def handle_query():
    console.print("\nQuery should be an artist name or language (punjabi, haryanvi, hindi)\nSpeacially 'unmatched' can be written to see unmatched songs.")
    q = input("Enter query (press Enter for default 'all'): ").strip()
    logger.info(f"User entered query: '{q}'")

    if q == "":
        logger.info("Default query selected: 'all'")
        return "all"

    elif q == 'unmatched':
        logger.info("Default query selected: 'unmatched'")
        return 'unmatched'

    q_lower = q.lower()
    valid_langs = {'punjabi', 'haryanvi', 'hindi'}
    valid_artists = set(artists['artist'].str.lower())

    if q_lower in valid_langs or q_lower in valid_artists:
        logger.info(f"Valid query: {q_lower}")
        return q_lower

    console.print(f"❌ Invalid query: '{q}'\nPlease enter a valid artist name or one of {list(valid_langs)}.")
    logger.warning(f"Invalid query entered: '{q}'")
    return None

def view_songs():
    query = handle_query()
    if query is None:
        return

    songs_data = songs('./data', query)
    
    # Handle case when query returns a string message
    if (songs_data is None):
        console.print("No songs found in dir")
        return

    if isinstance(songs_data, str):
        console.print(songs_data)
        logger.warning(f"Songs query returned message: {songs_data}")
        return

    # Use show_table directly with DataFrame data
    show_table(
        title=f"Songs for '{query}'",
        columns=list(songs_data.columns),
        rows=songs_data.values.tolist()
    )

    console.print(f"\nTotal number of songs: {len(songs_data)}")
    logger.info(f"Displayed {len(songs_data)} songs for query '{query}'")

def view_stats():
    all_songs = songs('./data', 'all')

    if (all_songs is None):
        console.print("No songs found in dir for analysis")
        return

    # Handle string messages returned by songs()
    if isinstance(all_songs, str):
        console.print(all_songs)
        logger.warning(f"Songs query returned message: {all_songs}")
        return

    statistics = stats(all_songs)
    print_dict(statistics, title="All Songs Statistics")
    logger.info("Displayed statistics for all songs")

def view_artists():
    q = input("Enter artist name or language (punjabi, haryanvi, hindi): ").strip()
    logger.info(f"User requested artist view: '{q}'")
    
    # If query is empty, show all artists
    if q == "":
        show_table(
            title="All Artists",
            columns=list(artists.columns),
            rows=artists.values.tolist()
        )
        console.print(f"\nTotal number of artists: {len(artists)}")
        logger.info(f"Displayed all {len(artists)} artists")
        return

    q_lower = q.lower()

    # Language filter
    if q_lower in ['punjabi', 'haryanvi', 'hindi']:
        lang_artists = artists[artists['language'] == q_lower].reset_index(drop=True)
        if not len(lang_artists):
            console.print(f"No artists found for language '{q}' 😷")
            logger.warning(f"No artists found for language '{q}'")
            return
        show_table(
            title=f"{q.capitalize()} Artists",
            columns=list(lang_artists.columns),
            rows=lang_artists.values.tolist()
        )
        console.print(f"\nNumber of {q.capitalize()} artists: {len(lang_artists)}")
        logger.info(f"Displayed {len(lang_artists)} {q} artists")
        return

    # Search by artist name (case-insensitive, partial match)
    matched_artists = artists[artists['artist'].str.lower().str.contains(q_lower)].reset_index(drop=True)
    if not len(matched_artists):
        console.print(f"No valid artist found matching '{q}' 😷")
        logger.warning(f"No artists matched query '{q}'")
        return

    show_table(
        title=f"Artists matching '{q}'",
        columns=list(matched_artists.columns),
        rows=matched_artists.values.tolist()
    )
    console.print(f"\nNumber of artists: {len(matched_artists)}")
    logger.info(f"Displayed {len(matched_artists)} artists matching '{q}'")

def download_songs_handler():
    download_list = pd.read_csv('./download_list.csv')

    # Use show_table with proper columns and rows
    show_table(
        title="Download List",
        columns=list(download_list.columns),
        rows=download_list.values.tolist()
    )

    console.print("\nTo add or remove songs edit download_list.csv in root directory\n")

    q = input("Enter 'y' to download songs: ").strip()
    if q.lower() != 'y':
        console.print("Download cancelled")
        logger.info("User cancelled download")
        return

    prefix = input("Enter prefix (press Enter for None): ").strip()
    confirm = input("Enter 'y' to remove previous prefixes: ").strip()

    if confirm.lower() == 'y':
        remove_prefixes('./data')
        logger.info("Previous prefixes removed")
        console.print("Previous prefixes removed ✅")
    else:
        console.print("No prefix operation")
        logger.info("Skipped prefix removal")

    logger.info(f"Download started with prefix '{prefix}'")
    console.print("Download started 🎵")
    download_songs(prefix)

    copy = input("Want to copy downloads folder to data folder? (y | n): ")
    if(copy.lower() == 'y'):
        copy_downloads()
        
    clear = input("Want to clear downloads folder? (y | n): ")
    if(clear.lower() == 'y'):
        clear_downloads()

def handle_scrape():
    i = input("Enter artist name or album you want to scrape: ")
    l = input("Enter language: ")
    search_youtube_songs(i, l)
    c = input("Want to copy scraped result to download_list.csv? (y | n): ")
    if(c.lower() == 'y'):
        df = pd.read_csv('./youtube_songs.csv')
        df.to_csv('./download_list.csv', index=False)
        console.print("Scraped result copied to download_list.csv")

def run():
    options = ['view songs', 'view stats', 'view artists', 'download songs', 'scrape']
    console.print("Welcome to GoMusic 🎵", style="")
    console.print("Select an option index eg: 0, 1, 2 etc")

    for idx, opt in enumerate(options):
        console.print(f"Option {idx}: {opt}")

    i = input("\nSelected option: ")

    try:
        i = int(i)
    except ValueError:
        console.print("Invalid option")
        logger.warning(f"Invalid option input: '{i}'")
        return

    match i:
        case 0:
            view_songs()
        case 1:
            view_stats()
        case 2: 
            view_artists()
        case 3:
            download_songs_handler()
        case 4:
            handle_scrape()
        case _:
            console.print("Invalid option")
            logger.warning(f"Option out of range: {i}")

if __name__ == "__main__":
    run()
