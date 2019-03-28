import numpy as np 
import pandas as pd

from  keras.models import Sequential, load_model
from sklearn.preprocessing import Normalizer, Binarizer

# read in csv data using pandas
testdata = pd.read_csv('Small Test Set.csv', header=None)
testdata_label = pd.read_csv('Small Test Set Target.csv', header=None)

# create a dataframe with testing data & testing label 
testdata = testdata.iloc[:, 0:37]
testdata_label = testdata_label.iloc[:, 38]

# normalize the data & convert dataframe to numpy array
scaler = Normalizer().fit(testdata)
testdata = scaler.transform(testdata)
np.set_printoptions(precision=3)

# reshape input to be [samples, time steps, features]
testdata_ar = np.reshape(testdata, (testdata.shape[0], 1, testdata.shape[1]))

# convert dataframe to numpy array & transfer 1-D array yo 2-D array
testdata_arlabel = np.array(testdata_label)
label_length = testdata_arlabel.shape[0]
testdata_arlabel = np.array(testdata_arlabel).reshape(label_length, 1)

# load model
model = Sequential()
model = load_model('lstm1layer_model.hdf5')
preds_train = model.predict(testdata_ar, verbose=1)

# save the result to csv 
result_datafram = pd.DataFrame(preds_train)
result_datafram.to_csv('result_o.csv', index=False, header=False, sep=',')

scaler = Binarizer(threshold=0.4)
preds_train = scaler.transform(preds_train)

# save the result to csv 
result_datafram = pd.DataFrame(preds_train)
result_datafram.to_csv('result.csv', index=False, header=False, sep=',')

# calculate the  accuracy
count = 0
for i in range(label_length):
    if(preds_train[i, 0]==testdata_arlabel[i, 0]):
        count += 1
print(count/label_length)