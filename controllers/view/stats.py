
from controllers.preprocess.data import merged_data

def stats(songs_list):
    df = merged_data(songs_list)
    
    if(df is None):
        print("No songs found in dir for analysis")
        return

    # Summary stats
    total_matched = len(df[df['language'].notna()])

    stat = {
        "total songs": int(len(df)),
        "punjabi songs": int(len(df[df['language'] == 'punjabi'])),
        "haryanvi songs": int(len(df[df['language'] == 'haryanvi'])),
        "hindi songs": int(len(df[df['language'] == 'hindi'])),
        "unmatched songs": int(df['language'].isna().sum()),
        "accuracy": str(float(round((total_matched/len(df) * 100),2))) + "%"
    }
    return stat


if __name__ == '__main__':
    from songs import songs 

    all_songs = songs('./data', 'all')
    print(stats(all_songs))
