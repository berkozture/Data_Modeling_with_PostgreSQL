import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *



#Inserts the records from the Song file into the Songs and Artists table
def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].fillna(-1).values[0].tolist()
    cur.execute(artist_table_insert, artist_data)

    
    
#Inserts records from the Log file into the Time, Songplays and Users table
def process_log_file(cur, filepath):
    # open log file
    df = pd.read_json(filepath, lines=True)
    df = df.drop_duplicates()

    # filter by NextSong action
    df = df.loc[df['page'] == 'NextSong', ['artist', 'page', 'auth', 'firstName', 'gender', 'itemInSession', 'lastName', 'length', 'level', 'location', 'method', 'page', 'registration', 'sessionId', 'song', 'status', 'ts', 'userAgent', 'userId']]

    # convert timestamp column to datetime
    #t =
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = df['ts'].dt.strftime('%Y-%m-%d %H:%M:%S, %H, %d, %U, %m, %Y, %A')
    time_data = time_data.str.split(', ', expand=True)
    time_data = [time_data.iloc[:, 0], time_data.iloc[:, 1], time_data.iloc[:, 2], time_data.iloc[:, 3], time_data.iloc[:, 4], time_data.iloc[:, 5], time_data.iloc[:, 5]]
    
    column_labels = ['timestamp', 'hour', 'day', 'week of year', 'month', 'year', 'weekday']
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))
    time_df = time_df.drop_duplicates()

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId', 'firstName', 'lastName', 'gender', 'level']]
    user_df = user_df.drop_duplicates()

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)



# Searches the current and child directories for the files and processes them iteratively
def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))



# Initiates the processing of thebtables
def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()

    

if __name__ == "__main__":
    main()