# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 18:57:42 2017

@author: Jun Hao
"""

#Neural Network classifier
from sklearn.neural_network import MLPClassifier
X = [[0., 0.], [1., 1.]]
y = [0, 1]
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)

print(clf.fit(X, y))

print(clf.predict([[2., 2.], [-1., -2.]]))

print([coef.shape for coef in clf.coefs_])

print(clf.predict_proba([[2., 2.], [1., 2.]]) )

X = [[0., 0.], [1., 1.]]
y = [[0, 1], [1, 1]]
clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(15,), random_state=1)

clf.fit(X, y)                         

print(clf.predict([[1., 2.]]))
 
print(clf.predict([[0., 0.]]))



import csv

with open('dataset-har-PUC-Rio-ugulino.csv') as csvfile:
    reader = csv.DictReader(csvfile)
#    for row in reader:
#        print(row)
      
# Encode output variable  
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
le.fit(['sitting-down', 'standing-up', 'standing', 'walking', 'sitting'])
print(list(le.classes_))
print(le.transform(['walking', 'standing','standing-up', 'sitting', 'sitting-down']))


#Evaluate model
from sklearn.svm import SVC
from sklearn.model_selection import KFold
from sklearn.metrics import confusion_matrix

kfold = KFold(n_splits=10, shuffle=True)

fold_index = 0
for train, test in kfold.split(normalized_X):
    svm_model_linear = SVC(kernel = 'linear', C = 1).fit(normalized_X[train], y[train])
    svm_predictions = svm_model_linear.predict(normalized_X[test])
    accuracy = svm_model_linear.score(normalized_X[test], y[test])
    cm = confusion_matrix(y[test], svm_predictions)
    print('In the %i fold, the classification accuracy is %f' %(fold_index, accuracy))
    print('And the confusion matrix is: ')
    print(cm)
    fold_index +=1
    