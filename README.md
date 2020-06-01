# Sparkify-relational

This is the first project in Udacity's Data Engineering Nanodegree.

In this project I played the role of the data engineer in Sparkify the music company to extract data from song files as well as from log file by users.
Song files are subset of [Million Song Dataset](http://millionsongdataset.com/) & log files are simulated by [eventsim](https://github.com/Interana/eventsim)

## Source Data.
Source data are JSON files divided into two groups, Song data and Log data. You can find the subset used for testing in `data/song_data` & `data/log_data`.

Below is the is sample of each type of data

```json
{"num_songs": 1, "artist_id": "ARD7TVE1187B99BFB1", "artist_latitude": null, "artist_longitude": null, "artist_location": "California - LA", "artist_name": "Casual", "song_id": "SOMZWCG12A8C13C480", "title": "I Didn't Mean To", "duration": 218.93179, "year": 0}
```

```json
{"artist":"N.E.R.D. FEATURING MALICE","auth":"Logged In","firstName":"Jayden","gender":"M","itemInSession":0,"lastName":"Fox","length":288.9922,"level":"free","location":"New Orleans-Metairie, LA","method":"PUT","page":"NextSong","registration":1541033612796.0,"sessionId":184,"song":"Am I High (Feat. Malice)","status":200,"ts":1541121934796,"userAgent":"\"Mozilla\/5.0 (Windows NT 6.3; WOW64) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"","userId":"101"}
{"artist":null,"auth":"Logged In","firstName":"Stefany","gender":"F","itemInSession":0,"lastName":"White","length":null,"level":"free","location":"Lubbock, TX","method":"GET","page":"Home","registration":1540708070796.0,"sessionId":82,"song":null,"status":200,"ts":1541122176796,"userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"","userId":"83"}
```
## ETL Pipeline
The ETL pipeline is Python 3 script with use of Pandas DataFrame to pocess data and PostgreSQL as RDBMS to store the output of the pipeline.

The data is processed from its JSON format and modeled as [Start Schema](https://en.wikipedia.org/wiki/Star_schema) with a single fact table `songplays` and 4 dimension tables `users`, `songs`, `artists` & `time`. 

- A row in the fact table `songplay` is based on user action `NextSong` from the log data.
- A row in `users` table is based on 'userId' from the log data. `userId` is the primary key and the DBMS handles conflicts by updating the user `level` if different
- A row in `time` table is based on timestaps `ts` in the log data. With the timestamp in milliseconds being the primary. Duplicates are rejected by the DBMS.
- A row in `songs` table is based on song data. Each song has a unique ID. 
- A row in the `artists` table is based also on the song data. Each artist has a unique ID used as primary key and the DBMS reject duplicates.

Below is DB schema and the first 5 rows of each table

![schema](https://github.com/OmarAlghamdi/Sparkify-relational/blob/master/diagrams/schema.png)
### songplays
![songplays table](https://github.com/OmarAlghamdi/Sparkify-relational/blob/master/diagrams/songplays-table.png)
### users
![users table](https://github.com/OmarAlghamdi/Sparkify-relational/blob/master/diagrams/users-table.png)
### time
![time table](https://github.com/OmarAlghamdi/Sparkify-relational/blob/master/diagrams/time-table.png)
### songs
![songs table](https://github.com/OmarAlghamdi/Sparkify-relational/blob/master/diagrams/songs-table.png)
### artists
![artists table](https://github.com/OmarAlghamdi/Sparkify-relational/blob/master/diagrams/artists-table.png)


## Dependncies
 - Python 3
 - Pandas
 - PostgreSQL
 - psycopg2
 - Jupyter Notbook (optional)
 - ipython-sql (optional)


## How To use it

- Install dependncies.
- Create a database in PostgreSQL with `sparkifydb` as its name.
- If you want to use different database name or if your DB credentials are different, then update the connection strings in `create_tables.py` & `etl.py`.
- Run the `create_tables.py` script to drop existing tables if any and create the fact and dimension tables.
- Run the `etl.py` script to process the data in the json file and insert data into the db.
- You can make sure that data have been processed corretly by using the `test.ipynb`notebook. You will need the optional dependncies for this.
- If you run the tests make sure to restart the kernal of the notebook since it blocks the access to the DB.



