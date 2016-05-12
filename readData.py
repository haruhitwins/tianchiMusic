# -*- coding: utf-8 -*-
"""
Created on Wed May 11 22:00:08 2016

@author: Haolin
"""
import sqlite3
import numpy as np

def readData():
    conn = sqlite3.connect('tianchiMusic.db')
    c = conn.cursor()
    c.execute('select * from data;')
    X, Y = [], []
    for row in c.fetchall():
        X.append([int(x) for x in row[1:-2]])# row = [song_id, ..., date, cnt]
        if row[-1] is None:
            Y.append(0)
        else:
            Y.append(int(row[-1]))
    conn.commit()
    conn.close()
    return np.array(X), np.array(Y)
    
if __name__ == '__main__':
    X, Y = readData()
    print X.shape
    print Y.shape