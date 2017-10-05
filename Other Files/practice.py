# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

print ('hello world')

from sklearn import datasets
from sklearn import svm

iris = datasets.load_iris()
digits = datasets.load_digits()
digits.target
print(digits.target) 
print(digits.data)  

clf = svm.SVC(gamma=0.001, C=100.)
clf.fit(digits.data[:-1], digits.target[:-1])

clf.predict(digits.data[-1:])

print(digits.target) 
print(digits.data)  