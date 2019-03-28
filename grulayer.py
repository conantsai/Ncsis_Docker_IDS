from keras.models import Sequential
from keras.layers import Dense, Dropout, GRU, Activation

def CreateGRU():
    # define the network
    # create model 
    model = Sequential()
    model.add(GRU(32,input_dim=37, return_sequences=True))  # try using a GRU instead, for fun
    model.add(Dropout(0.2))
    model.add(GRU(32, return_sequences=True))  # try using a GRU instead, for fun
    model.add(Dropout(0.2))
    model.add(GRU(32, re2urn_sequences=True))  # try using a GRU instead, for fun
    model.add(Dropout(0.2))
    model.add(GRU(32, return_sequences=False))  # try using a GRU instead, for fun
    model.add(Dropout(0.2))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    return model