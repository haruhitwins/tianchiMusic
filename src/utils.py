# -*- coding: utf-8 -*-
"""
Created on Sun May 22 17:23:08 2016

@author: Haolin
"""

import pandas as pd

def splitData(data, isTest=True, pickUp=None):
    dataHasLabel = data[: 50 * 183].values
    X = dataHasLabel[:, :-5]
    if type(pickUp) == int:
        y = dataHasLabel[:, pickUp]
    else:
        y = dataHasLabel[:, -5]
    if isTest:
        split = 153 * 50
        trainX, trainY, testX, testY = X[:split], y[:split], X[split:], y[split:]
        return trainX, trainY, testX, testY
    else:
        testX = data[50 * 183 + 50: ]#Plus 50 to skip 8/31
        testX = testX[data.columns[: -5]]
        return X, y, testX, None
        
def output(clf, testX):
    finalY = pd.Series(data=clf.predict(testX), index=testX.index).sortlevel().apply(lambda x: int(x + 0.5))
    output = pd.DataFrame(finalY, columns=['y']).reset_index(level=1)[['y', 'date']]
    output.to_csv('../out/result.csv', header=False)
    
def outputCombine(y3, y2, y1, y0, index):
    y = y3 * 1000 + y2 * 100 + y1 * 10 + y0
    finalY = pd.Series(data=y, index=index).sortlevel().apply(lambda x: int(x + 0.5))
    output = pd.DataFrame(finalY, columns=['y']).reset_index(level=1)[['y', 'date']]
    output.to_csv('../out/result.csv', header=False)