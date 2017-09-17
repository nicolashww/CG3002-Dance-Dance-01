# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 18:57:42 2017

@author: Jun Hao
"""
#simple timer
import time
tfulls = time.time()

import csv
import numpy as np 

#Sort data into columns -> For some reason can't extract class column using the better(next) method
with open('dataset-har-PUC-Rio-ugulino.csv') as csvfile:
    reader=csv.reader(csvfile,delimiter=';')
    headers = next(reader)
    column = {}
    for h in headers:
        column[h] = []
    for row in reader:
        for h, v in zip(headers, row):
            column[h].append(v)

#Sort data into a whole array and extract necessary data
testdata = np.genfromtxt ('dataset-har-PUC-Rio-ugulino.csv', delimiter=";")
testdata = np.delete(testdata, (0), axis=0)
X = testdata[:,[6,7,8,9,10,11,12,13,14,15,16,17]]


#Data pre-processing
from sklearn import preprocessing

##Encode output variable  
le = preprocessing.LabelEncoder()
le.fit(['sittingdown', 'standingup', 'standing', 'walking', 'sitting'])
#print(list(le.classes_))
y = []
y = le.transform(column['class'])

#Normalize data
normalized_X = preprocessing.normalize(X) 


#Evaluate model
from sklearn.svm import SVC
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix

kfold = KFold(n_splits=10, shuffle=True)

fold_index = 0
for train, test in kfold.split(normalized_X):
    tparts = time.time()
    svm_model_linear = SVC(kernel = 'linear', C = 1).fit(normalized_X[train], y[train])
    svm_predictions = svm_model_linear.predict(normalized_X[test])
    accuracy = svm_model_linear.score(normalized_X[test], y[test])
    cm = confusion_matrix(y[test], svm_predictions)
    tparte = time.time()
    print('In the %i fold, the classification accuracy is %f' %(fold_index, accuracy))
    print('And the confusion matrix is: ')
    print(cm)
    print('This fold took %f seconds END' %(tparte-tparts))
    fold_index +=1
    
tfulle = time.time()
print('The whole code took %f seconds' %(tfulle-tfulls))
    
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
