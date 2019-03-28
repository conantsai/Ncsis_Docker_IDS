from loaddata import LoadTrainData
from lstmlayer import CreateLSTM
from rnnlayer import CreateRNN
from grulayer import CreateGRU

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

traindata_arX, traindata_arY, testdata_arX, testdata_arY, validdata_arX, validdata_arY= LoadTrainData()
model = CreateLSTM()

# compile model using mse as a measure of model performance
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
# train model
history = model.fit(traindata_arX, traindata_arY, batch_size=32, nb_epoch=20, validation_data=(testdata_arX, testdata_arY))
model.save("lstmlayera20_model.hdf5")
DrawTrendChart(history)

