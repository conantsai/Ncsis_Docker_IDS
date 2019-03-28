import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import Normalizer

# read in csv data using pandas
data = pd.read_csv('Tuesday-WorkingHours.csv')

relabel = data[' Label'].copy()
relabel[relabel != 'BENIGN'] = 0
relabel[relabel == 'BENIGN'] = 1
data[' Label'] = relabel

data = data.drop(['Flow ID', ' Source IP', ' Destination IP', ' Timestamp'], axis = 1)
traindata = data.sample(frac=0.9, random_state=7)
testdata = data.loc[~data.index.isin(traindata.index)]
validdata = traindata.sample(frac=0.1, random_state=17)

traindata = traindata.astype(np.float32)
print(data)