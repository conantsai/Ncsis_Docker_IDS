from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM, Activation

def CreateLSTM():
    # define the network
    # create model 
    model = Sequential()
    # add model layers
    model.add(LSTM(32,input_dim=77, return_sequences=True))  # try using a GRU instead, for fun
    model.add(Dropout(0.2))
    model.add(LSTM(32, return_sequences=True))  # try using a GRU instead, for fun
    model.add(Dropout(0.2))
    model.add(LSTM(32, return_sequences=False))  # try using a GRU instead, for fun
    model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))

    return model