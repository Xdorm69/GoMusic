import pandas as pd

def all_artists(query='all'):
    artist = pd.read_csv('../../constants/artists.csv')
    if query == 'all':
        return artist