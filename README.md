# Project 1: Data modeling with Postgres
Sparkify, a music streaming startup has been collecting data on songs and user activity through their streaming app using JSON files.
### Purpose
The purpose of the project is
- to set up a Postgres database and to model the song and log datasets (JSON files) to create relevant FACT and DIMENSION tables using a STAR schema. The tables need to be designed in an optimized way (atleast 2 NF form) so that song analysis queries can be run easily

- to design an ETL pipeline which will extract data from the JSON logs and metadata to load the data into the tables

- The analytical goal of this schema is to analyze the songs that the users are listening like frequently listened songs, their durations, time of day when songs are played, which artists are more popular.

### Database Schema design (STAR Schema)

Below image shows the Star Schema for the Sparkify database

![Sparkify Star Schema](https://github.com/abhishekrathgit/Postgres-Modelling-ETL-Pipeline/blob/main/Sparkify%20Postgres%20Database%20Star%20Schema.JPG "Sparkify Star Schema")

>Note:
 - Sparkify Postgres Database Star Schema.JPG is in the same repository with all other .py files
 - It can also be accesses from the below GitHub link:
   https://github.com/abhishekrathgit/Postgres-Modelling-ETL-Pipeline/blob/main/Sparify%20Postgres%20Database%20Star%20Schema.JPG

- The STAR schema contains **1 FACT** table (fact_songplays) & **4 DIMENSION** tables (dim_users, dim_songs, dim_artists, dim_time)

- All tables are in **2nd Normal form**
- Table columns with datatypes and Primary Key are defined below

| fact_songplays        |dim_users         |dim_songs           |dim_artists           |dim_time
|-----------------------|------------------|--------------------|----------------------|-------
|songplay_id SERIAL (PK)|user_id INT (PK)  |song_id VARCHAR (PK)|artist_id VARCHAR (PK)|start_time TIMESTAMP (PK)
|start_time timestamp   |first_name VARCHAR|title VARCHAR       |name VARCHAR          |hour INT
|user_id INT            |last_name VARCHAR |artist_id VARCHAR   |location VARCHAR      |day INT
|level VARCHAR          |gender CHAR(1)    |year INT            |latitude FLOAT        |week INT
|song_id VARCHAR        |level VARCHAR     |duration FLOAT      |longitude FLOAT       |month INT
|artist_id VARCHAR      |                  |                    |                      |year INT
|session_id INT         |                  |                    |                      |weekday INT
|location VARCHAR
|user_agent VARCHAR

### Data Format
`data/song_data` and `data/log_data`
### ETL Pipeline
1. **sql_queries.py** contains `DROP TABLE`, `CREATE TABLE`, `INSERT` and `SELECT` queries for all tables

2. **create_tables.py** has functions `create_database` to create **Sparkify** database. It also has `create_tables` and `drop_tables` functions to `DROP` and `CREATE` fact and dimension tables by using sql_queries.py
3. Extract, Load & Transformation is done in **etl.py**
    - `process_data` function is defined to extract all the **JSON** filepaths from `data/song_data` and `data/log_data` directories

    - `process_song_file` function is used to load **dim_songs** and **dim_artists** from `data/song_data`
    - `process_log_file` function is used to load **dim_users** from `data/log_data`by filtering `page` column with `NextSong` values. **dim_time** is populated from the `timestamp` column from log data.
    - **fact_songplays** is loaded by deriving columns from log file data and by joining dim_songs and dim_artists to get `song_id` and `artist_id` using a `SELECT` query from sql_queries.py

4. `test.ipynb` contains `SELECT` queries to test if tables are loaded properly and how many rows are inserted


### Files Execution and Permisions granted
1. `create_tables.py` and `etl.py` were made executable in terminal by using `chmod +x` command
2. `#!/usr/bin/env python3` was added to both .py files to make it run as default in python3

#### Order of Execution
.py files were executed in Terminal followed by .ipynb files
1. `./create_tables.py`
2. `./etl.py`
3. `test.ipynb`
4. `Analytical_Dashboard.ipynb`

### Dashboard for analytic queries
`Analytical_Dashboard.ipynb` contains 3 analytical queries and output.

1. Query to find the count number of Subscribers by Subscription type

  `SELECT level as "Subscription Type", COUNT(*) as "# Subscribers" FROM dim_users group by 1;`

2. Query to find the fequencies of song listned on any day of the week

  `SELECT weekday, case when weekday = 0 then 'Mon' when weekday = 1 then 'Tue'   when weekday = 2 then 'Wed' when weekday = 3 then 'Thur' when weekday   = 4 then 'Fri' when weekday = 5 then 'Sat' when weekday = 6 then  'Sun' end as "Day", COUNT(*) as "# Songs listened" FROM dim_time group by 1 order by 1;`

3. Query to find which artist by their popularity popular (whose songs are listened to more frequently)

  `SELECT a.artist_id, b.name, b.location, sum(a.duration) from dim_songs a LEFT  JOIN dim_artists b ON a.artist_id = b.artist_id group by 1,2,3 order by 4 desc`
