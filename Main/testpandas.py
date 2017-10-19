import pandas as pd
import numpy as np
import csv
from sklearn import preprocessing

with open('training_cleaned.csv') as csvfile:
    reader=csv.reader(csvfile,delimiter=';')
    headers = next(reader)
    column = {}
    for h in headers:
        column[h] = []
    for row in reader:
        for h, v in zip(headers, row):
            column[h].append(v)
            
##Encode output variable
le = preprocessing.LabelEncoder()
le.fit(['sittingdown', 'standingup', 'standing', 'walking', 'sitting'])
#print(list(le.classes_))
y = []
y = le.transform(column['class'])

def avg(myArray, N=5):
    cum = np.cumsum(myArray,0)
    result = cum[N-1::N]/float(N)
    result[1:] = result[1:] - result[:-1]

    remainder = myArray.shape[0] % N
    if remainder != 0:
        if remainder < myArray.shape[0]:
            lastAvg = (cum[-1]-cum[-1-remainder])/float(remainder)
        else:
            lastAvg = cum[-1]/float(remainder)
        result = np.vstack([result, lastAvg])

    return result

print (y[:10])
print ((avg(y[:10])).astype(int))
print ((np.around((avg(y[:10])), decimals=1)).astype(int))



pdtestdata = pd.read_csv('training_cleaned.csv', delimiter=';')
pdtestdata = pdtestdata.drop(pdtestdata.columns[12], axis=1)
pdtestdata = pdtestdata[:10]
print (pdtestdata.columns)
#print pdtestdata[:5]


averagedata = pdtestdata.groupby(np.arange(len(pdtestdata))//5).mean()
#averagedata['class'] = ((avg(y[:10])).astype(int)).tolist()




all12data = np.reshape(pdtestdata.values,(2,60))





pdtestdata.to_csv('testinglol.csv')
hello = pdtestdata.as_matrix()
hello = hello#[[0,1,2,3,4,5,6,7,8], :]
print (hello)

print('AVERAGED')
hello2 = averagedata.as_matrix()
hello2 = hello2
print (hello2)

print('COMBINED')
#hello3 = all12data.as_matrix()
hello3 = all12data
print (hello3)