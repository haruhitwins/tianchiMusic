# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 11:15:32 2016

@author: Haolin
"""

import sqlite3

if __name__ == '__main__':
    ACTION_TABLE = 'mars_tianchi_user_actions'
    SONG_TABLE = 'mars_tianchi_songs'
    
    conn = sqlite3.connect('../tianchiMusic.db')
    c = conn.cursor()
    
    c.execute('SELECT COUNT(*) FROM %s;' % ACTION_TABLE)
    print 'Total rows from %s: ' % ACTION_TABLE, c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM %s;' % SONG_TABLE)
    print 'Total rows from %s: ' % SONG_TABLE, c.fetchone()[0]
    
    c.execute('SELECT COUNT(DISTINCT song_id) FROM %s;' % ACTION_TABLE)
    print 'Total songs from %s: ' % ACTION_TABLE, c.fetchone()[0]

    c.execute('SELECT COUNT(DISTINCT song_id) FROM %s;' % SONG_TABLE)
    print 'Total songs from %s: ' % SONG_TABLE, c.fetchone()[0]
    
    c.execute('SELECT COUNT(DISTINCT user_id) FROM %s;' % ACTION_TABLE)
    print 'Total users: ', c.fetchone()[0]
    
    c.execute('SELECT COUNT(DISTINCT artist_id) FROM %s WHERE gender = 1;' % SONG_TABLE)
    print 'Artist counts of gender 1: ', c.fetchone()[0]
    c.execute('SELECT COUNT(DISTINCT artist_id) FROM %s WHERE gender = 2;' % SONG_TABLE)
    print 'Artist counts of gender 2: ', c.fetchone()[0]
    c.execute('SELECT COUNT(DISTINCT artist_id) FROM %s WHERE gender = 3;' % SONG_TABLE)
    print 'Artist counts of gender 3: ', c.fetchone()[0]
    c.execute('SELECT COUNT(DISTINCT artist_id) FROM %s;' % SONG_TABLE)
    print 'Total artists: ', c.fetchone()[0]
    
    c.execute('SELECT DISTINCT language FROM %s;' % SONG_TABLE)
    cnt = 0
    for row in c.fetchall():
        cnt += 1
        c.execute('SELECT COUNT(*) FROM %s WHERE language = ?;' % SONG_TABLE, row)
        print 'Song counts of language %d:' % row[0], c.fetchone()[0]
    print 'Total languages: ', cnt
    
    c.execute('SELECT AVG(cnt) FROM (SELECT COUNT(DISTINCT song_id) AS cnt FROM %s GROUP BY artist_id);' % SONG_TABLE)
    print 'Average songs per artist: ', c.fetchone()[0]
    
    c.execute('SELECT AVG(cnt) FROM (SELECT COUNT(*) AS cnt FROM %s WHERE action_type = 1 GROUP BY song_id);' % ACTION_TABLE)
    print 'Average plays per song: ', c.fetchone()[0]
    
    c.execute('SELECT AVG(cnt) FROM (SELECT COUNT(*) AS cnt FROM %s WHERE action_type = 2 GROUP BY song_id);' % ACTION_TABLE)
    print 'Average downloads per song: ', c.fetchone()[0]
    
    c.execute('SELECT AVG(cnt) FROM (SELECT COUNT(*) AS cnt FROM %s WHERE action_type = 3 GROUP BY song_id);' % ACTION_TABLE)
    print 'Average collects per song: ', c.fetchone()[0]
    
    c.execute('SELECT AVG(cnt) FROM (SELECT COUNT(*) AS cnt FROM %s WHERE action_type = 1 GROUP BY user_id);' % ACTION_TABLE)
    print 'Average plays per user: ', c.fetchone()[0]
    
    c.execute('SELECT AVG(cnt) FROM (SELECT COUNT(*) AS cnt FROM %s WHERE action_type = 2 GROUP BY user_id);' % ACTION_TABLE)
    print 'Average downloads per user: ', c.fetchone()[0]
    
    c.execute('SELECT AVG(cnt) FROM (SELECT COUNT(*) AS cnt FROM %s WHERE action_type = 3 GROUP BY user_id);' % ACTION_TABLE)
    print 'Average collects per user: ', c.fetchone()[0]
    
    c.execute('SELECT AVG(song_init_plays) FROM %s;' % SONG_TABLE)
    print 'Average init_plays per song: ', c.fetchone()[0]    
    
    c.execute('SELECT AVG(cnt) FROM (SELECT COUNT(song_id) AS cnt FROM %s GROUP BY publish_time);' % SONG_TABLE)
    print 'Average song releases per day: ', c.fetchone()[0] 
    
    conn.close()