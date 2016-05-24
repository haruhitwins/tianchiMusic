# -*- coding: utf-8 -*-
"""
Created on Sun May 22 17:20:48 2016

@author: Haolin
"""
import pandas as pd
import numpy as np
from sklearn import ensemble
from sklearn.metrics import accuracy_score
from utils import splitData, output

params = {'n_estimators': 500, 'max_leaf_nodes': 4, 'max_depth': None,
          'min_samples_split': 5, 'learning_rate': 0.1, 'subsample': 0.5}

if __name__ == '__main__':
    data = pd.read_csv('../out/artists_all_features.csv', index_col=['artist_id', 'date'])
    data.sortlevel(level=1, inplace=True)
    clf = ensemble.GradientBoostingClassifier(**params)
    
    trainX, trainY, testX, testY = splitData(data, pickUp=-4)    
    clf.fit(trainX, trainY)
    print accuracy_score(testY, clf.predict(testX))
    
    X, y, testX, _ = splitData(data, isTest=False, pickUp=-4)    
    clf.fit(X, y)
    y3 = clf.predict(testX)
    
    trainX, trainY, testX, testY = splitData(data, pickUp=-3)    
    clf.fit(trainX, trainY)
    print accuracy_score(testY, clf.predict(testX))
    
    X, y, testX, _ = splitData(data, isTest=False, pickUp=-3)    
    clf.fit(X, y)
    y2 = clf.predict(testX)
    
    trainX, trainY, testX, testY = splitData(data, pickUp=-2)    
    clf.fit(trainX, trainY)
    print accuracy_score(testY, clf.predict(testX))
    
    X, y, testX, _ = splitData(data, isTest=False, pickUp=-2)    
    clf.fit(X, y)
    y1 = clf.predict(testX)
    
    trainX, trainY, testX, testY = splitData(data, pickUp=-1)    
    clf.fit(trainX, trainY)
    print accuracy_score(testY, clf.predict(testX))
    
    X, y, testX, _ = splitData(data, isTest=False, pickUp=-1)    
    clf.fit(X, y)
    y0 = clf.predict(testX)