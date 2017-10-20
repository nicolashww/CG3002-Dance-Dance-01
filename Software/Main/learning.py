# -*- coding: utf-8 -*-
"""
@author: Jun Hao
"""

#Set print command to print to file
import sys
sys.stdout = open("Output.txt", "w")

#Print current time on computer
from datetime import datetime
print (str(datetime.now()))

#Implement simple timer
import time
tfulls = time.time()


#Sort data into columns -> For some reason can't extract class column using the better(next) method
import csv
import numpy as np
with open('dataset_FULL.csv') as csvfile:
    reader=csv.reader(csvfile,delimiter=';')
    headers = next(reader)
    column = {}
    for h in headers:
        column[h] = []
    for row in reader:
        for h, v in zip(headers, row):
            column[h].append(v)

#Sort data into a whole array and extract necessary data
testdata = np.genfromtxt ('dataset_CLEANED.csv', delimiter=";")
testdata = np.delete(testdata, (0), axis=0)
X = testdata[:,[1,2,3,4,5,6,7,8,9,10,11,12]]


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
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix

n_splits_val = 10
kfold = KFold(n_splits=n_splits_val, shuffle=True)

#KNN
print(' ')
print('Nearest Neighbors')
print(' ')
tknns = time.time()
fold_index = 0
avg_accuracy_knn = 0
for train, test in kfold.split(normalized_X, y=None, groups=None):
    tparts = time.time()
    knn_model = KNeighborsClassifier(n_neighbors=5, weights='uniform', algorithm='auto', leaf_size=30, p=2, metric='minkowski', metric_params=None, n_jobs=-1).fit(normalized_X[train], y[train])
    knn_predictions = knn_model.predict(normalized_X[test])
    accuracy = knn_model.score(normalized_X[test], y[test])
    cm = confusion_matrix(y[test], knn_predictions)
    tparte = time.time()
    avg_accuracy_knn += accuracy
    print('In the %i fold, the classification accuracy is %f' %(fold_index, accuracy))
    print('And the confusion matrix is: ')
    print(cm)
    print('This fold took %f seconds' %(tparte-tparts))
    fold_index +=1
    print(' ')
avg_accuracy_knn /= n_splits_val
tknne = time.time()

#RF
print(' ')
print('Random Forest')
print(' ')
trfs = time.time()
fold_index = 0
avg_accuracy_rf = 0
for train, test in kfold.split(normalized_X, y=None, groups=None):
    tparts = time.time()
    rf_model = RandomForestClassifier(n_jobs=-1).fit(normalized_X[train], y[train])
    rf_predictions = rf_model.predict(normalized_X[test])
    accuracy = rf_model.score(normalized_X[test], y[test])
    cm = confusion_matrix(y[test], rf_predictions)
    tparte = time.time()
    avg_accuracy_rf += accuracy
    print('In the %i fold, the classification accuracy is %f' %(fold_index, accuracy))
    print('And the confusion matrix is: ')
    print(cm)
    print('This fold took %f seconds' %(tparte-tparts))
    fold_index +=1
    print(' ')
avg_accuracy_rf /= n_splits_val
trfe = time.time()
print(' ')

#Results
print('Results:')
print(' ')
print('Nearest Neighbors took %f seconds' %(tknne-tknns))
print('with an average accuracy of %f%%' %(avg_accuracy_knn*100))
print(' ')
print('Random Forest took %f seconds' %(trfe-trfs))
print('with an average accuracy of %f%%' %(avg_accuracy_rf*100))
print(' ')
print(' ')


#Extract some random values
sample = normalized_X[[100,57759,66113,116595,134393],:]
sampletruth = y[[100,57759,66113,116595,134393],]

print('Sample data(normalized):')
print(sample)
print(' ')
print('Correct result:')
print(sampletruth)
print('KNN predicted result:')
print(knn_model.predict(sample))
print('RF predicted result:')
print(rf_model.predict(sample))


#Save models for deployment use
#from sklearn.externals import joblib
#joblib.dump(knn_model, 'model_knn.pkl') #Save Model
#knn_model = joblib.load('model_knn.pkl') #Load Model
#joblib.dump(rf_model, 'model_rf.pkl') #Save Model
#rf_model = joblib.load('model_rf.pkl') #Load Model

#
tfulle = time.time()
print('The whole code took %f seconds' %(tfulle-tfulls))
