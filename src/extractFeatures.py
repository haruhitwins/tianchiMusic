# -*- coding: utf-8 -*-
"""
Created on Mon May 09 19:26:29 2016

@author: Haolin
"""

import sqlite3
from datetime import datetime
from datetime import timedelta

languageCodeBook = {0:0, 1:1, 2:2, 3:3, 4:4, 11:5, 12:6, 14:7, 100:8}
dbPath = '../tianchiMusic.db'

def createSongsDate(): 
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    CREATE_STATEMENT = '''CREATE TABLE songs_date
                          (song_id TEXT,
                           date TEXT,
                           age INTEGER,
                           isHoliday INTEGER,
                           weekday INTEGER
                          )'''
    c.execute(CREATE_STATEMENT)
    conn.commit()
    
    res = []
    holidays = [datetime(2015, 4, 5), datetime(2015, 5, 1), datetime(2015, 6, 20), 
                datetime(2015, 9, 27), datetime(2015, 10, 1)]
    oneDay = timedelta(1)
    endDate = datetime(2015, 8, 30)
    c.execute('SELECT song_id, publish_time FROM filtered_songs;')   
    cnt = 0
    for row in c.fetchall():
        if cnt % 1000 == 0:
            print cnt
        cnt += 1
        date = datetime(2015, 3, 1)
        song_id = row[0]
        publish = datetime.strptime(row[1], '%Y%m%d')
        while date <= endDate:
            age = (date - publish).days #Might be negative
            isHoliday = 1 if date in holidays else 0
            weekday = date.weekday()
            res.append((song_id, date.strftime('%Y%m%d'), age, isHoliday, weekday))
            date += oneDay
            
    c.executemany('INSERT INTO songs_date VALUES (?,?,?,?,?)', res)
    conn.commit()
    conn.close()    

def createSongsPartialFeature():
    """
    song_id: [6 months action1, 6 months action2, 6 months action3, 
              7 weekdays action1, 7 weekdays action2, 7 weekdays action3]
    """   
    res = {}
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    
    print 'SELECT song_id FROM filtered_songs;'
    c.execute('SELECT song_id FROM filtered_songs;')   
    for row in c.fetchall():        
        song_id = row[0]
        res[song_id] = [0] * 39
        
    print 'SELECT * FROM songs_action_counts_per_month;'
    c.execute('SELECT * FROM songs_action_counts_per_month;')   
    for row in c.fetchall():
        song_id, month, action_type, cnt = row[0], int(row[1]), int(row[2]), int(row[3])
        res[song_id][(action_type - 1) * 6 + (month - 3)] = cnt
        
    print 'SELECT * FROM songs_action_counts_per_weekday;'
    c.execute('SELECT * FROM songs_action_counts_per_weekday;')   
    for row in c.fetchall():
        song_id, weekday, action_type, cnt = row[0], int(row[1]), int(row[2]), int(row[3])
        res[song_id][(action_type - 1) * 7 + weekday + 18] = cnt

    insertValues = []        
    for song_id, feature in res.iteritems():
        if sum(feature) == 0:
            print song_id
        feature.insert(0, song_id)
        insertValues.append(tuple(feature))
    
    CREATE_STATEMENT = '''CREATE TABLE songs_partial_feature
                          (song_id TEXT,
                           m31 INTEGER,
                           m41 INTEGER,
                           m51 INTEGER,
                           m61 INTEGER,
                           m71 INTEGER,
                           m81 INTEGER,
                           m32 INTEGER,
                           m42 INTEGER,
                           m52 INTEGER,
                           m62 INTEGER,
                           m72 INTEGER,
                           m82 INTEGER,
                           m33 INTEGER,
                           m43 INTEGER,
                           m53 INTEGER,
                           m63 INTEGER,
                           m73 INTEGER,
                           m83 INTEGER,
                           w01 INTEGER,
                           w11 INTEGER,
                           w21 INTEGER,
                           w31 INTEGER,
                           w41 INTEGER,
                           w51 INTEGER,
                           w61 INTEGER,
                           w02 INTEGER,
                           w12 INTEGER,
                           w22 INTEGER,
                           w32 INTEGER,
                           w42 INTEGER,
                           w52 INTEGER,
                           w62 INTEGER,
                           w03 INTEGER,
                           w13 INTEGER,
                           w23 INTEGER,
                           w33 INTEGER,
                           w43 INTEGER,
                           w53 INTEGER,
                           w63 INTEGER
                          )'''
    c.execute(CREATE_STATEMENT)
    c.executemany('INSERT INTO songs_partial_feature VALUES (' + ','.join(['?'] * 40) + ')', insertValues)
    conn.commit()
    conn.close() 
    print 'Done.' 

def runSqlScript(fileName):
    """
    This method would be VERY SLOW.
    Recommend to run script in cmd using sqlite3.
    """
    conn = sqlite3.connect(dbPath)
    c = conn.cursor()
    with open(fileName) as f:
        c.executescript(f.read())
    conn.commit()
    conn.close()


if __name__ == '__main__':
    runSqlScript('sqlScript1.sql')
    createSongsDate()
    createSongsPartialFeature()
    runSqlScript('sqlScript2.sql')
    """
    Final features in table 'songs_feature' (1863489 rows).
    Label in table 'song_plays_everyday' (424521 rows).
    """