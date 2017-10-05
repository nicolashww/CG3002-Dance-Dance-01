# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 18:57:42 2017

@author: Jun Hao
"""
#simple timer
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
testdata = np.genfromtxt ('dataset_FULL.csv', delimiter=";")
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
#from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix

n_splits_val = 10
kfold = KFold(n_splits=n_splits_val, shuffle=True)

##SVM
#print('Support Vector Machines')
#print(' ')
#tsvms = time.time()
#fold_index = 0
#avg_accuracy_svm = 0
#for train, test in kfold.split(normalized_X):
#    tparts = time.time()
#    #SVC vs SVM
#    #LinearSVC is not linear SVM. If you scale it up too much - it will also fail, as now tolerance and number of iterations are crucial. Do not use LinearSVC.
#    svm_model_linear = SVC(kernel = 'linear', C = 1).fit(normalized_X[train], y[train])
#    svm_predictions = svm_model_linear.predict(normalized_X[test])
#    accuracy = svm_model_linear.score(normalized_X[test], y[test])
#    cm = confusion_matrix(y[test], svm_predictions)
#    tparte = time.time()
#    avg_accuracy_svm += accuracy
#    print('In the %i fold, the classification accuracy is %f' %(fold_index, accuracy))
#    print('And the confusion matrix is: ')
#    print(cm)
#    print('This fold took %f seconds' %(tparte-tparts))
#    fold_index +=1
#    print(' ')
#avg_accuracy_svm /= n_splits_val
#tsvme = time.time()

#NN
print(' ')
print('Neural network model')
print(' ')
tnns = time.time()
fold_index = 0
avg_accuracy_nn = 0
for train, test in kfold.split(normalized_X):
    tparts = time.time()
    nn_model = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1).fit(normalized_X[train], y[train])
    nn_predictions = nn_model.predict(normalized_X[test])
    accuracy = nn_model.score(normalized_X[test], y[test])
    cm = confusion_matrix(y[test], nn_predictions)
    tparte = time.time()
    avg_accuracy_nn += accuracy
    print('In the %i fold, the classification accuracy is %f' %(fold_index, accuracy))
    print('And the confusion matrix is: ')
    print(cm)
    print('This fold took %f seconds' %(tparte-tparts))
    fold_index +=1
    print(' ')
avg_accuracy_nn /= n_splits_val
tnne = time.time()

#KNN
print(' ')
print('Nearest Neighbors')
print(' ')
tknns = time.time()
fold_index = 0
avg_accuracy_knn = 0
for train, test in kfold.split(normalized_X):
    tparts = time.time()
    knn_model = KNeighborsClassifier().fit(normalized_X[train], y[train])
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

#AB
print(' ')
print('AdaBoost')
print(' ')
tabs = time.time()
fold_index = 0
avg_accuracy_ab = 0
for train, test in kfold.split(normalized_X):
    tparts = time.time()
    ab_model = AdaBoostClassifier().fit(normalized_X[train], y[train])
    ab_predictions = ab_model.predict(normalized_X[test])
    accuracy = ab_model.score(normalized_X[test], y[test])
    cm = confusion_matrix(y[test], ab_predictions)
    tparte = time.time()
    avg_accuracy_ab += accuracy
    print('In the %i fold, the classification accuracy is %f' %(fold_index, accuracy))
    print('And the confusion matrix is: ')
    print(cm)
    print('This fold took %f seconds' %(tparte-tparts))
    fold_index +=1
    print(' ')
avg_accuracy_ab /= n_splits_val
tabe = time.time()

#RF
print(' ')
print('Random Forest')
print(' ')
trfs = time.time()
fold_index = 0
avg_accuracy_rf = 0
for train, test in kfold.split(normalized_X):
    tparts = time.time()
    rf_model = RandomForestClassifier().fit(normalized_X[train], y[train])
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
#print(' ')
#print('Support Vector Machines took %f seconds' %(tsvme-tsvms))
#print('with an average accuracy of %f%%' %(avg_accuracy_svm*100))
print(' ')
print('Neural network model took %f seconds' %(tnne-tnns))
print('with an average accuracy of %f%%' %(avg_accuracy_nn*100))
print(' ')
print('Nearest Neighbors took %f seconds' %(tknne-tknns))
print('with an average accuracy of %f%%' %(avg_accuracy_knn*100))
print(' ')
print('AdaBoost took %f seconds' %(tabe-tabs))
print('with an average accuracy of %f%%' %(avg_accuracy_ab*100))
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
#print('SVM predicted result:')
#print(svm_model_linear.predict(sample))
print('NN predicted result:')
print(nn_model.predict(sample))
print('KNN predicted result:')
print(knn_model.predict(sample))
print('AB predicted result:')
print(ab_model.predict(sample))
print('RF predicted result:')
print(rf_model.predict(sample))
    
tfulle = time.time()
print('The whole code took %f seconds' %(tfulle-tfulls))
