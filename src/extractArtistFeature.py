# -*- coding: utf-8 -*-
"""
Created on Wed May 18 18:00:36 2016

@author: Haolin
"""

import pandas as pd
import numpy as np

DURATION_DAYS = 183.0
HOLIDAYS = set(['20150405', '20150501', '20150620', '20150927', '20151001',\
                '20150403', '20150430', '20150619', '20150926', '20150930',\
                '20150404', '20150502', '20150621', '20150928', '20151002'])

def totalWeekdaysDuring(start='20150301', end='20150830'):
    startTimestamp = pd.Timestamp(start)
    endTimestamp = pd.Timestamp(end)
    totalDays = (endTimestamp - startTimestamp).days + 1
    a, b = totalDays / 7, totalDays % 7
    startWeekday = startTimestamp.weekday()
    res = [a] * 7
    for i in xrange(b):
        res[(startWeekday + i) % 7] += 1
    return res

def extractArtistFeature():
    songDF = pd.read_csv('../dataSource/mars_tianchi_songs.csv', index_col='song_id')
    df = pd.DataFrame(index=songDF['artist_id'].unique())
    df['songsCnt'] = songDF.groupby('artist_id')['gender'].count()
    df['initPlaysMean'] = songDF.groupby('artist_id')['song_init_plays'].mean()
    df['initPlaysStd'] = songDF.groupby('artist_id')['song_init_plays'].std()
    gender = songDF.groupby('artist_id')['gender'].mean()
    df['gender1'] = gender.apply(lambda x: int(x == 1))
    df['gender2'] = gender.apply(lambda x: int(x == 2))
    df['gender3'] = gender.apply(lambda x: int(x == 3))
    del gender
    language = songDF.groupby('artist_id')['language'].unique()
    for i in [0, 1, 2, 3, 4, 11, 12, 14, 100]:
        df['language%d' % i] = language.apply(lambda x : int(i in x))
    del language
    songDF['publish_time'] = songDF['publish_time'].apply(lambda x: pd.Timestamp(str(x)).to_julian_date())
    df['songBornDateMean'] = songDF.groupby('artist_id')['publish_time'].mean()
    
    actionDF = pd.read_csv('../dataSource/mars_tianchi_user_actions.csv')
    actionDF = pd.merge(actionDF, songDF, how='left', left_on='song_id', right_index=True)
    del songDF
    action1DF = actionDF[actionDF['action_type'] == 1]
    action2DF = actionDF[actionDF['action_type'] == 2]
    action3DF = actionDF[actionDF['action_type'] == 3]
    
    df['songPlaysPerDayMean'] = action1DF.groupby('artist_id')['gender'].count() / DURATION_DAYS
    EX2 = action1DF.groupby(['artist_id', 'ds']).count()['gender'].apply(lambda x: x*x).groupby(level='artist_id').sum() / DURATION_DAYS
    EX_2 = df['songPlaysPerDayMean'].apply(lambda x: x*x)
    df['songPlaysPerDayStd'] = (EX2 - EX_2).apply(np.sqrt)

    df['songDownloadsPerDayMean'] = action2DF.groupby('artist_id')['gender'].count() / DURATION_DAYS
    EX2 = action2DF.groupby(['artist_id', 'ds']).count()['gender'].apply(lambda x: x*x).groupby(level='artist_id').sum() / DURATION_DAYS
    EX_2 = df['songDownloadsPerDayMean'].apply(lambda x: x*x)
    df['songDownloadsPerDayStd'] = (EX2 - EX_2).apply(np.sqrt)

    df['songCollectsPerDayMean'] = action3DF.groupby('artist_id')['gender'].count() / DURATION_DAYS
    EX2 = action3DF.groupby(['artist_id', 'ds']).count()['gender'].apply(lambda x: x*x).groupby(level='artist_id').sum() / DURATION_DAYS
    EX_2 = df['songCollectsPerDayMean'].apply(lambda x: x*x)
    df['songCollectsPerDayStd'] = (EX2 - EX_2).apply(np.sqrt)
    del EX2, EX_2
    
    uniqueUsers1 = action1DF.groupby('artist_id')['user_id'].unique()
    df['playedUsersCnt'] = uniqueUsers1.apply(lambda x: len(x))
    uniqueUsers2 = action2DF.groupby('artist_id')['user_id'].unique()
    df['downloadedUsersCnt'] = uniqueUsers2.apply(lambda x: len(x))
    uniqueUsers3 = action3DF.groupby('artist_id')['user_id'].unique()
    df['collectedUsersCnt'] = uniqueUsers3.apply(lambda x: len(x))
    
    uniqueUsers1 = pd.DataFrame(uniqueUsers1)
    uniqueUsers2 = pd.DataFrame(uniqueUsers2)
    uniqueUsers3 = pd.DataFrame(uniqueUsers3)
    tmp1 = pd.merge(uniqueUsers1, uniqueUsers2, left_index=True, right_index=True)
    tmp2 = pd.merge(uniqueUsers1, uniqueUsers3, left_index=True, right_index=True)
    tmp3 = pd.merge(uniqueUsers2, uniqueUsers3, left_index=True, right_index=True)
    del uniqueUsers1, uniqueUsers2
    df['playedDownloadedUsersCnt'] = tmp1.apply(lambda x: len(set(x[0]).intersection(set(x[1]))), axis=1)
    df['playedCollectedUsersCnt'] = tmp2.apply(lambda x: len(set(x[0]).intersection(set(x[1]))), axis=1)    
    df['downloadedCollectedUsersCnt'] = tmp3.apply(lambda x: len(set(x[0]).intersection(set(x[1]))), axis=1)
    del tmp2, tmp3
    tmp = pd.merge(tmp1, uniqueUsers3, left_index=True, right_index=True)
    del tmp1, uniqueUsers3
    df['allActionsUsersCnt'] = tmp.apply(lambda x: len(set(x[0]).intersection(set(x[1])).intersection(set(x[2]))), axis=1)
    del tmp
    
#    action1DF['ds'] = action1DF['ds'].apply(lambda x: pd.Timestamp(str(int(x))))
    action1DF['weekday'] = action1DF['ds'].apply(lambda x: pd.Timestamp(str(int(x))).dayofweek)
    weekdaysCnt = totalWeekdaysDuring()
    for i in xrange(7):
        tmp = action1DF[action1DF['weekday'] == i]
        df['songPlaysDay%dMean' % i] = tmp.groupby('artist_id')['gender'].count() / weekdaysCnt[i]
        EX2 = tmp.groupby(['artist_id', 'ds']).count()['gender'].apply(lambda x: x*x).groupby(level='artist_id').sum() / weekdaysCnt[i]
        EX_2 = df['songPlaysDay%dMean' % i].apply(lambda x: x*x)
        df['songPlaysDay%dStd' % i] = (EX2 - EX_2).apply(np.sqrt)
    del tmp, EX2, EX_2
    
    df.to_csv('../out/artists_features.csv', index_label='artist_id')

def combineDateFeatures():
    df = pd.read_csv('../out/artists_features.csv')    
    day = pd.Timestamp('20150301')
    end = pd.Timestamp('20151030')
    one = pd.Timedelta(days=1)
    dates = []
    while day <= end:
        dates.append(day.strftime('%Y%m%d'))
        day += one
    
    import itertools
    tmp = []
    artists = df['artist_id'].tolist()
    for comb in itertools.product(artists, dates):
        tmp.append(comb)
    features = pd.DataFrame(tmp, columns=['artist_id', 'date'])
    features = pd.merge(features, df, on='artist_id')
    tmp = features['date'].apply(lambda x: pd.Timestamp(x).to_julian_date())
    features['songsAgeMean'] = tmp - features['songBornDateMean']
    features['weekday'] = features['date'].apply(lambda x: pd.Timestamp(x).dayofweek)
    features['isHoliday'] = features['date'].apply(lambda x: int(x in HOLIDAYS))
    features['month'] = features['date'].apply(lambda x: pd.Timestamp(x).month)
    features['day'] = features['date'].apply(lambda x: pd.Timestamp(x).day)
    
    songDF = pd.read_csv('../dataSource/mars_tianchi_songs.csv')
    actionDF = pd.read_csv('../dataSource/mars_tianchi_user_actions.csv')
    actionDF = actionDF[actionDF['action_type'] == 1]
    actionDF['ds'] = actionDF['ds'].apply(lambda x: str(int(x)))
    actionDF = pd.merge(actionDF, songDF, how='left', on='song_id')
    plays = actionDF.groupby(['artist_id', 'ds'])['gender'].count()
    del actionDF, songDF
    features = features.set_index(['artist_id', 'date'])
    features['y'] = plays
    features.loc[pd.isnull(features['y']), 'y'] = 0
    features['y3'] = (features['y'] / 1000).astype(int) % 10
    features['y2'] = (features['y'] / 100).astype(int) % 10
    features['y1'] = (features['y'] / 10).astype(int) % 10
    features['y0'] = features['y'].astype(int) % 10
    features.to_csv('../out/artists_all_features.csv', index_label=['artist_id', 'date'])
    
if __name__ == '__main__':
    combineDateFeatures()