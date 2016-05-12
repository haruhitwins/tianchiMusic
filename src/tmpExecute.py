# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 13:13:47 2016

@author: Haolin
"""
import sqlite3

if __name__ == '__main__':
    res = {}
    with open('artist_plays_everyday.csv') as f:
        f.next()
        for l in f:
            l = l.strip().split(',')
            if not l[0] in res:
                res[l[0]] = int(l[2])
            else:
                res[l[0]] += int(l[2])
    for artist in res:
        print artist, res[artist]/183.0
#    ACTION_TABLE = 'mars_tianchi_user_actions'
#    SONG_TABLE = 'mars_tianchi_songs'
#    
#    conn = sqlite3.connect('tianchiMusic.db')
#    c = conn.cursor()
#    
#    c.execute('SELECT AVG(cnt) FROM (SELECT COUNT(song_id) AS cnt FROM %s GROUP BY publish_time);' % SONG_TABLE)
#    print 'Average song releases per day: ', c.fetchone()[0]   
#    
#    conn.close()
