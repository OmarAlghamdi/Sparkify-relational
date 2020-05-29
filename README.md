# Sparkify-relational

This is the first project in Udacity's Data Engineering Nanodegree.

In this project I played the role of the data engineer in Sparkify the music company to extract data from song files as well as from log file by users.
Song files are subset of [Million Song Dataset](http://millionsongdataset.com/) & log files are simulated by [eventsim](https://github.com/Interana/eventsim)

PostgreSQL is used as database. Data modeled as Star Schema.

![schema](https://github.com/OmarAlghamdi/Sparkify-relational/blob/master/diagrams/shema.png)

## Dependncies
 - Python 3
 - Jupyter Notbook
 - PostgreSQL
 - ipython-sql
 - psycopg2


## How To use it

- Install dependncies
- Run the 'create_tables' script to drop existing tables if any and create table
- Run the 'etl' script to process the data in the json file and insert data into the db
- You can make sure that data have been processed corretly by using the 'test' notebook


