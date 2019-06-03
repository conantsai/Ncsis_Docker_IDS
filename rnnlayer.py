from keras.models import Sequential
from keras.layers import Dense, Dropout, SimpleRNN, Activation

def CreateRNN():
    # define the network
    # create model
    model = Sequential()
    # add model layers
    model.add(SimpleRNN(32,input_dim=77, return_sequences=True))  # try using a GRU instead, for fun
    model.add(Dropout(0.1))
    model.add(SimpleRNN(32, return_sequences=True))  # try using a GRU instead, for fun
    model.add(Dropout(0.1))
    model.add(SimpleRNN(32, return_sequences=True))  # try using a GRU instead, for fun
    model.add(Dropout(0.1))
    model.add(SimpleRNN(32, return_sequences=False))  # try using a GRU instead, for fun
    model.add(Dropout(0.1))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    return model