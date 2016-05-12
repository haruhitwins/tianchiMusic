# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 10:31:36 2016

@author: Haolin
"""

import sqlite3

if __name__ == '__main__':
    conn = sqlite3.connect('tianchiMusic.db')
    c = conn.cursor()
    
    CREATE_ACTIONS = '''CREATE TABLE mars_tianchi_user_actions
                        (
                        user_id TEXT, 
                        song_id TEXT, 
                        gmt_create INTEGER, 
                        action_type INTEGER, 
                        Ds TEXT
                        )'''
                        
    CREATE_SONGS = '''CREATE TABLE mars_tianchi_songs
                      (
                      song_id TEXT, 
                      artist_id TEXT, 
                      publish_time TEXT, 
                      song_init_plays INTEGER, 
                      Language INTEGER, 
                      Gender INTEGER
                      )'''
    
    c.execute(CREATE_ACTIONS)
    c.execute(CREATE_SONGS)
    conn.commit()
    
    res = []
    with open('dataSource/mars_tianchi_user_actions.csv') as f:
        for l in f:
            ls = l.strip().split(',')
            res.append((ls[0], ls[1], int(ls[2]), int(ls[3]), ls[4]))
            
    if res:
        c.executemany('INSERT INTO mars_tianchi_user_actions VALUES (?,?,?,?,?)', res)
        conn.commit()
        
    res = []
    with open('dataSource/mars_tianchi_songs.csv') as f:
        for l in f:
            ls = l.strip().split(',')
            res.append((ls[0], ls[1], ls[2], int(ls[3]), int(ls[4]), int(ls[5])))
            
    if res:
        c.executemany('INSERT INTO mars_tianchi_songs VALUES (?,?,?,?,?,?)', res)
        conn.commit()
    
    conn.close()