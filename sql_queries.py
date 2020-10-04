# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS fact_songplays;"
user_table_drop = "DROP TABLE IF EXISTS dim_users;"
song_table_drop = "DROP TABLE IF EXISTS dim_songs;"
artist_table_drop = "DROP TABLE IF EXISTS dim_artists;"
time_table_drop = "DROP TABLE IF EXISTS dim_time;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS fact_songplays (
    songplay_id SERIAL, 
    start_time timestamp, 
    user_id INT, 
    level VARCHAR, 
    song_id VARCHAR, 
    artist_id VARCHAR, 
    session_id INT, 
    location VARCHAR, 
    user_agent VARCHAR,
    PRIMARY KEY (songplay_id)
    );
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_users (
    user_id INT, 
    first_name VARCHAR, 
    last_name VARCHAR, 
    gender CHAR(1), 
    level VARCHAR,
    PRIMARY KEY(user_id)
    );
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_songs (
song_id VARCHAR, 
title VARCHAR, 
artist_id VARCHAR, 
year INT, 
duration FLOAT,
PRIMARY KEY (song_id)
    );
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_artists (
    artist_id VARCHAR, 
    name VARCHAR, 
    location VARCHAR, 
    latitude FLOAT, 
    longitude FLOAT,
    PRIMARY KEY (artist_id)
    );
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_time (
    start_time TIMESTAMP, 
    hour INT, 
    day INT, 
    week INT, 
    month INT, 
    year INT, 
    weekday INT,
    PRIMARY KEY (start_time)
    );
""")

# INSERT RECORDS

songplay_table_insert = ("""
INSERT INTO fact_songplays (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
INSERT INTO dim_users (user_id, first_name, last_name, gender, level)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (user_id) 
DO UPDATE
    SET level = excluded.level
""")

song_table_insert = ("""
INSERT INTO dim_songs (song_id, title, artist_id, year, duration)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (song_id)
DO NOTHING
""")


artist_table_insert = ("""
INSERT INTO dim_artists (artist_id, name, location, latitude, longitude)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (artist_id) 
DO NOTHING
""")


time_table_insert = ("""
INSERT INTO dim_time (start_time, hour, day, week, month, year, weekday)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
""")

# FIND SONGS

song_select = ("""
SELECT a.song_id, b.artist_id
    FROM dim_songs a
    inner join 
    dim_artists b
        ON a.artist_id = b.artist_id
        WHERE a.title = %s 
        AND b.name = %s 
        AND a.duration = %s;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]