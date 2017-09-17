# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 18:57:42 2017

@author: Jun Hao
"""

#Neural Network classifier
#from sklearn.neural_network import MLPClassifier
#X = [[0., 0.], [1., 1.]]
#y = [0, 1]
#clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
#
#print(clf.fit(X, y))
#
#print(clf.predict([[2., 2.], [-1., -2.]]))
#
#print([coef.shape for coef in clf.coefs_])
#
#print(clf.predict_proba([[2., 2.], [1., 2.]]) )
#
#X = [[0., 0.], [1., 1.]]
#y = [[0, 1], [1, 1]]
#clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1)
#
#clf.fit(X, y)                         
#
#print(clf.predict([[1., 2.]]))
# 
#print(clf.predict([[0., 0.]]))

import csv
import numpy as np 

with open('dataset-har-PUC-Rio-ugulino.csv') as csvfile:
    reader=csv.reader(csvfile,delimiter=';')
    headers = next(reader)
    column = {}
    for h in headers:
        column[h] = []
    for row in reader:
        for h, v in zip(headers, row):
            column[h].append(v)
    

#Data pre-processing

# Encode output variable  
#from sklearn import preprocessing
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
le.fit(['sittingdown', 'standingup', 'standing', 'walking', 'sitting'])
#print(list(le.classes_))



X = np.vstack((preprocessing.normalize(column['x1']), preprocessing.normalize(column['y1']), preprocessing.normalize(column['z1']), preprocessing.normalize(column['x2']), preprocessing.normalize(column['y2']), preprocessing.normalize(column['z2']), preprocessing.normalize(column['x3']), preprocessing.normalize(column['y3']), preprocessing.normalize(column['z3']), preprocessing.normalize(column['x4']), preprocessing.normalize(column['y4'])))
print(X)
y = []
y = le.transform(column['class'])
print(y)



#Evaluate model
from sklearn.svm import SVC
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix

kfold = KFold(n_splits=10, shuffle=True)

fold_index = 0
for train, test in kfold.split(X):
    svm_model_linear = SVC(kernel = 'linear', C = 1).fit(X[train], y[train])
    svm_predictions = svm_model_linear.predict(X[test])
    accuracy = svm_model_linear.score(X[test], y[test])
    cm = confusion_matrix(y[test], svm_predictions)
    print('In the %i fold, the classification accuracy is %f' %(fold_index, accuracy))
    print('And the confusion matrix is: ')
    print(cm)
    fold_index +=1
    