# -*- coding: utf-8 -*-
"""
Created on Sun May 22 17:25:28 2016

@author: Haolin
"""
import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
from utils import splitData

if __name__ == '__main__':
    data = pd.read_csv('../out/artists_all_features.csv', index_col=['artist_id', 'date'])
    data.sortlevel(level=1, inplace=True) 
    trainX, trainY, testX, testY = splitData(data)
    clf = linear_model.LassoCV(max_iter=5000)
    clf.fit(trainX, trainY)
    mse = mean_squared_error(testY, clf.predict(testX))
    print("MSE: %.4f" % mse)
    sortedCoef = np.sort(clf.coef_)
    argSoredCoef = np.argsort(clf.coef_)
    print sortedCoef
    print argSoredCoef