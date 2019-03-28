import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import Normalizer

from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Activation

# read in csv data using pandas
traindata = pd.read_csv('KDDTrain+.csv', header=None)
testdata = pd.read_csv('KDDTest+.csv', header=None)

# create a dataframe with all training data & testing data except the target column 
traindata_X = traindata.iloc[:, 0:37]
traindata_Y = traindata.iloc[:, 38]
testdata_X = testdata.iloc[:, 0:37]
testdata_Y = testdata.iloc[:, 38]

# normalize the data & convert dataframe to numpy array
scaler = Normalizer().fit(traindata_X)
traindata_X = scaler.transform(traindata_X)
np.set_printoptions(precision=3)

scaler = Normalizer().fit(testdata_X)
testdata_X = scaler.transform(testdata_X)
np.set_printoptions(precision=3)

# convert dataframe to numpy array
traindata_arY = np.array(traindata_Y)
testdata_arY = np.array(testdata_Y)

# reshape input to be [samples, time steps, features]
traindata_arX = np.reshape(traindata_X, (traindata_X.shape[0], 1, traindata_X.shape[1]))
testdata_arX = np.reshape(testdata_X, (testdata_X.shape[0], 1, testdata_X.shape[1]))

# define the network
# create model 
model = Sequential()
# add model layers
model.add(LSTM(32,input_dim=37, return_sequences=True))  # try using a GRU instead, for fun
model.add(Dropout(0.1))
model.add(LSTM(32, return_sequences=True))  # try using a GRU instead, for fun
model.add(Dropout(0.1))
model.add(LSTM(32, return_sequences=False))  # try using a GRU instead, for fun
model.add(Dropout(0.1))
model.add(Dense(1, activation='sigmoid'))
# print(model.get_config())

# compile model using mse as a measure of model performance
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
# train model
history = model.fit(traindata_arX, traindata_arY, batch_size=32, nb_epoch=100, validation_data=(testdata_arX, testdata_arY))
model.save("lstm1layer_model.hdf5")

# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.show()