#view existing songs
import os
import pandas as pd

from controllers.preprocess.data import merged_data

def songs(path='../../data', query='all'):
    try:
        valid_path = os.listdir(path)
    except FileNotFoundError:
        return "Path not found 🤷 creata a data folder in root dir"
    
    files = []
    for file in valid_path:
        if file.endswith(".mp3"):
            files.append(file)
    
    df = merged_data(files)
    if query == 'all':
        return df.reset_index(drop=True)
    elif query == 'punjabi':
        return df[df['language'] == 'punjabi'].reset_index(drop=True)
    elif query == 'haryanvi':
        return df[df['language'] == 'haryanvi'].reset_index(drop=True)
    elif query == 'hindi':
        return df[df['language'] == 'hindi'].reset_index(drop=True)
    else:
        q_lower = query.lower()
        artists = pd.read_csv('./constants/artists.csv')
        artists_list = artists['artist'].str.lower().tolist()
        if q_lower not in artists_list:
            return "Query not found 🤷"

        main = df[df['artist'].str.lower() == q_lower].reset_index(drop=True)

        if(not len(main)): 
            return "No songs found for this artist 🤷"
            
        return main
        