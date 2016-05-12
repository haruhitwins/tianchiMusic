# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 16:29:17 2016

@author: Haolin
"""
import datetime
import math

BEGIN_YEAR = 2015
BEGIN_MONTH = 9
BEGIN_DAY = 1
DURATION = 60

def predict(artist, day):
    return 0

def generateResult(artists, fileName='mars_tianchi_artist_plays_predict.csv'):
    oneDay = datetime.timedelta(1)
    with open(fileName,'w') as f:
        for artist in artists:
            day = datetime.date(BEGIN_YEAR, BEGIN_MONTH, BEGIN_DAY)            
            for _ in xrange(DURATION):
                cnt = predict(artist, day)
                f.write(','.join([artist, str(cnt), day.strftime('%Y%m%d')]) + '\n')
                day += oneDay
    print 'Done'    

def readResultFile(fileName):
    """
    File format:
    artist_id,plays,date
    """
    res = {}
    with open(fileName) as f:
        for l in f:
            l = l.strip().split(',')
            if not l[0] in res:
                res[l[0]] = {}
            res[l[0]][l[2]] = l[1]
    return res
    
def evaluate(predict, true):
    """
    Params predict and true should be dicts from readResultFile()
    Caculation details see:
    https://tianchi.shuju.aliyun.com/competition/information.htm?spm=5176.100067.5678.2.bJmdGF&raceId=231531
    """
    artists = predict.keys()
    dates = predict[artists[0]].keys()    
    Fi = 0.0
    for artist in artists:
        s, weight = 0.0, 0.0
        for date in dates:
            Tjk, Sijk = float(true[artist][date]), float(predict[artist][date])
            s += ((Tjk - Sijk) / Tjk) ** 2
            weight += Tjk
        sigmaij = math.sqrt(s / len(dates))
        phij = math.sqrt(weight)
        Fi += (1 - sigmaij) * phij
    return Fi

if __name__ == '__main__':
    print evaluate(readResultFile('mars_tianchi_artist_plays_predict.csv'), readResultFile('mars_tianchi_artist_plays_predict.csv'))
#    res = {}
#    with open('artist_plays_everyday.csv') as f:
#        f.next()
#        for l in f:
#            l = l.strip().split(',')
#            if not l[0] in res:
#                res[l[0]] = int(l[2])
#            else:
#                res[l[0]] += int(l[2])
#                
#    oneDay = datetime.timedelta(1)
#    with open('mars_tianchi_artist_plays_predict.csv','w') as f:
#        for artist in res:
#            day = datetime.date(2015, 9, 1)            
#            for _ in xrange(60):
#                f.write(','.join([artist, str(res[artist]/183), day.strftime('%Y%m%d')]) + '\n')
#                day += oneDay
#    print 'Done'