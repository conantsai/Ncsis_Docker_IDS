from loaddata import LoadTrainData
from lstmlayer import CreateLSTM
from rnnlayer import CreateRNN
from grulayer import CreateGRU
from test import test

import matplotlib.pyplot as plt

def DrawTrendChart(history):
    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper right')
    plt.show()

    # summarize history for accuracy
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper right')
    plt.show()

traindata_arX, traindata_arY, testdata_arX, testdata_arY, validdata_arX, validdata_arY = LoadTrainData()

modelrnn = CreateRNN()

# compile model using mse as a measure of model performance
modelrnn.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
# train model
historyrnn = modelrnn.fit(traindata_arX, traindata_arY, batch_size=32, nb_epoch=100, validation_data=(testdata_arX, testdata_arY))
modelrnn.save("rnnlayera100_model.hdf5")
DrawTrendChart(historyrnn)

modellstm = CreateLSTM()

# compile model using mse as a measure of model performance
modellstm.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
# train model
historylstm = modellstm.fit(traindata_arX, traindata_arY, batch_size=32, nb_epoch=100, validation_data=(testdata_arX, testdata_arY))
modellstm.save("lstmlayera100_model.hdf5")
DrawTrendChart(historylstm)

# acc_rnn, acc_lstm, count_loss = test(testdata_arX, testdata_arY)
# print(acc_rnn, acc_lstm, count_loss)

