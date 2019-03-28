import pandas as pd
import numpy as np 

from keras.models import Sequential
from keras.layers import Dense, LSTM, RNN, Dropout
from keras.optimizers import Adam
from keras.losses import mean_squared_error
from keras.callbacks import EarlyStopping

# read in csv data using pandas
traindata_tus = pd.read_csv('test.csv')
# create a dataframe with all training data except the target column "Label"
traindata_tusX = traindata_tus.drop(columns=[' Label'])
# convert dataframe to numpy array
traindata_tusX = traindata_tusX.values
# create a dataframe with only the target column "Label"
traindata_tusY = traindata_tus[[' Label']]
traindata_tusY = traindata_tusY.values

# # convert string to int
# for index in range(0, 10):
#     #convert sourev ip
#     data_sourceip = traindata_tus[' Source_IP'][index]
#     # data_sourceip = data_sourceip.replace('.', '')
#     # traindata_tus[' Source_IP'][index] =data_sourceip
#     sourceip1, sourceip2 ,sourceip3, sourceip4 = data_sourceip.split('.',3)

# reshape input to be [samples, time steps, features]
traindata_tusX = np.reshape(traindata_tusX, (traindata_tusX.shape[0], 1, traindata_tusX.shape[1]))

#get number of columns in training data
train_cols = traindata_tusX.shape[1]

# create model 
model = Sequential()
# add model layers
model.add(LSTM(units=32, activation='tanh', return_sequences=False, stateful=False, batch_input_shape=(traindata_tusX.shape[0], 1, traindata_tusX.shape[2])))
# model.add(Dropout(0.2))
# model.add(LSTM(units=32, activation='tanh', return_sequences=False, stateful=False))
# model.add(Dropout(0.2))
# model.add(LSTM(units=32, activation='tanh', return_sequences=False, stateful=False))
# model.add(Dropout(0.2))
model.add(Dense(units=1, activation='sigmoid'))
# compile model using mse as a measure of model performance
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.summary()

# # set early stopping monitor so the model stops training when it won't improve anymore
# early_stopping_monitor = EarlyStopping(patience=3)
# train model
model.fit(traindata_tusX, traindata_tusY, batch_size=3, epochs=30, verbose=2, validation_split=0.2)

