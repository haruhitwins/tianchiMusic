# -*- coding: utf-8 -*-
"""
Created on Fri May 20 19:08:33 2016

@author: Haolin
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn import ensemble
from sklearn.metrics import mean_squared_error
from utils import splitData, output

params = {'n_estimators': 300, 'max_depth': 4, 'min_samples_split': 1,
          'learning_rate': 0.01, 'loss': 'ls'}
    
def train_test_plot(data, plot=False):
    trainX, trainY, testX, testY = splitData(data)
    clf = ensemble.GradientBoostingRegressor(**params)
    clf.fit(trainX, trainY)
    mse = mean_squared_error(testY, clf.predict(testX))
    print("MSE: %.4f" % mse)
    
    if plot:
        ###############################################################################
        # Plot training deviance
        
        # compute test set deviance
        test_score = np.zeros((params['n_estimators'],), dtype=np.float64)
        
        for i, y_pred in enumerate(clf.staged_predict(testX)):
            test_score[i] = clf.loss_(testY, y_pred)
        
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 2, 1)
        plt.title('Deviance')
        plt.plot(np.arange(params['n_estimators']) + 1, clf.train_score_, 'b-',
                 label='Training Set Deviance')
        plt.plot(np.arange(params['n_estimators']) + 1, test_score, 'r-',
                 label='Test Set Deviance')
        plt.legend(loc='upper right')
        plt.xlabel('Boosting Iterations')
        plt.ylabel('Deviance')
        
    return clf

if __name__ == '__main__':
    data = pd.read_csv('../out/artists_all_features.csv', index_col=['artist_id', 'date'])
    data.sortlevel(level=1, inplace=True)
    
    clf = train_test_plot(data)
    
    sortedFeatureImportances = np.sort(clf.feature_importances_)
    print sortedFeatureImportances
    argsortedFeatureImportances = np.argsort(clf.feature_importances_)
    print argsortedFeatureImportances

    cnt = 0
    while sortedFeatureImportances[cnt] < 1e-2:
        cnt += 1
    cols = data.columns
    for i in xrange(cnt):
        col = cols[argsortedFeatureImportances[i]]
        print 'del %s' % col
        del data[col]
        
    clf = train_test_plot(data)
        
    X, y, testX, _ = splitData(data, isTest=False)
    clf = ensemble.GradientBoostingRegressor(**params)
    clf.fit(X, y)
#    predictY = clf.predict(testX)
#    for i,v in enumerate(predictY):
#        if i % 50 == 0:
#            print v
    output(clf, testX)