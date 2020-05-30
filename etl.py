import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    # opens json file as Pandas DataFrame
    df = pd.read_json(filepath, lines=True)

    # selects and inserts song record
    song_data = df.loc[:, ['song_id', 'artist_id',
                           'year', 'duration', 'title']].values.tolist()[0]
    cur.execute(song_table_insert, song_data)

    # selects and inserts artist record
    artist_data = df.loc[:, ['artist_id', 'artist_name', 'artist_location',
                             'artist_latitude', 'artist_longitude']].values.tolist()[0]
    cur.execute(artist_table_insert, artist_data)


def transform_month(m):
    # maps month to its name
    months = {
        1: 'January',
        2: 'Fabruary',
        3: 'March',
        4: 'April',
        5: 'May',
        6: 'June',
        7: 'July',
        8: 'August',
        9: 'September',
        10: 'October',
        11: 'November',
        12: 'December',
    }
    return months.get(m)


def transform_weekday(wd):
    # maps weekday to it name
    weekdays = {
        0: 'Monday',
        1: 'Tuesday',
        2: 'Wednesday',
        3: 'Thursday',
        4: 'Friday',
        5: 'Saturday',
        6: 'Sunday'
    }
    return weekdays.get(wd)


def process_log_file(cur, filepath):
    # opens json log file as Pandas DataFrame
    df = pd.read_json(filepath, lines=True)

    # selects only NextSong actions
    df = df.loc[df['page'] == 'NextSong']

    # extracts only timestamps from the logs as numpy.datatime
    ts = df.loc[:, 'ts']
    ts.drop_duplicates(inplace=True)
    t = ts.apply(pd.to_datetime)

    # creates Pandas DataFrame of time data
    time_data = {'timestamp': ts.values, 'hour': t.dt.hour.values, 'day': t.dt.day.values,
                 'week': t.dt.week.values, 'month': t.dt.month.values, 'year': t.dt.year.values, 'weekday': t.dt.weekday}

    time_df = pd.DataFrame(time_data)

    # tranforms numerical month and weekday columns into text
    time_df.month = time_df['month'].transform(transform_month)
    time_df.weekday = time_df['weekday'].transform(transform_weekday)

    # inserts time records into the database
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # selects and insert user records
    user_df = df.loc[:, ['userId', 'firstName', 'lastName', 'gender', 'level']]
    user_df.drop_duplicates(inplace=True)

    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    for index, row in df.iterrows():

        # gets songid and artistid from song and artist tables
        results = cur.execute(song_select, (row.song, row.artist, row.length))
        songid, artistid = results if results else None, None

        # inserts songplay record
        songplay_data = (row.ts, row.userId, row.level, songid,
                         artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    # reads json file in the given directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # prints total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterates over files and processes them
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    # connects to the database
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=sparkifydb user=postgres password=root")
    cur = conn.cursor()

    # processes song files
    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    # processes log files
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
