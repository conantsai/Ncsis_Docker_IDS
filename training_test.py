import numpy as np 
import pandas as pd

from  keras.models import Sequential, load_model
from sklearn.preprocessing import Normalizer, Binarizer

def test(testdata_ar, testdata_label):

##### testdata preprocessing #######################################################################################
    # # read in csv data using pandas
    # testdata = pd.read_csv(cvefile_path)
    # testdata_label = pd.read_csv(cvefile_path)

    # # replace string to int on ' Label'
    # relabel = testdata_label[' Label'].copy()
    # relabel[relabel != 'BENIGN'] = 0
    # relabel[relabel == 'BENIGN'] = 1
    # testdata_label[' Label'] = relabel

    # reflowpackets = testdata[' Flow Packets/s'].copy()
    # reflowpackets[reflowpackets == 'Infinity'] = 0
    # testdata[' Flow Packets/s']  = reflowpackets

    # # delete columns which has string value
    # testdata = testdata.drop(['Flow ID', ' Source IP', ' Destination IP', ' Timestamp', 'Flow Bytes/s', ' Flow Packets/s', ' Label'], axis = 1)

    # # create a dataframe with testing data & testing label 
    # testdata = testdata.iloc[:, 0:77]
    # origiontest = testdata
    # testdata_label = testdata_label.iloc[:, 84]

    # # normalize the data & convert dataframe to numpy array
    # scaler = Normalizer().fit(testdata)
    # testdata = scaler.transform(testdata)
    # np.set_printoptions(precision=3)

    # # reshape input to be [samples, time steps, features]
    # testdata_ar = np.reshape(testdata, (testdata.shape[0], 1, testdata.shape[1]))

    # convert dataframe to numpy array & transfer 1-D array yo 2-D array
    testdata_arlabel = np.array(testdata_label)
    label_length = testdata_arlabel.shape[0]
    testdata_arlabel = np.array(testdata_arlabel).reshape(label_length, 1)

##### testdata preprocessing #######################################################################################

##### rnn predict ##################################################################################################    
    # load rnn model
    model_rnn = Sequential()
    model_rnn = load_model('rnnlayera10_model.hdf5')
    preds_rnn = model_rnn.predict(testdata_ar, verbose=1)

    # save the rnn result without threshold to csv 
    resultdataN_rnn = pd.DataFrame(preds_rnn)
    resultdataN_rnn.to_csv('resultN_rnn.csv', index=False, header=False, sep=',')

    scaler_rnn = Binarizer(threshold=0.9)
    preds_rnn = scaler_rnn.transform(preds_rnn)

    # save the rnn result to csv 
    resultdata_rnn = pd.DataFrame(preds_rnn)
    resultdata_rnn.to_csv('result_rnn.csv', index=False, header=False, sep=',')

    # calculate the rnn accuracy
    count_rnn = 0
    for i in range(label_length):
        if(preds_rnn[i, 0]==testdata_arlabel[i, 0]):
            count_rnn += 1
    acc_rnn = count_rnn/label_length

##### rnn predict ################################################################################################## 

##### lstm predict #################################################################################################
    # load lstm model
    model_lstm = Sequential()
    model_lstm = load_model('lstmlayera10_model.hdf5')
    preds_lstm  = model_lstm.predict(testdata_ar, verbose=1)

    # save the lstm result without threshold to csv 
    resultdataN_lstm = pd.DataFrame(preds_lstm)
    resultdataN_lstm.to_csv('resultN_lstm.csv', index=False, header=False, sep=',')

    scaler_lstm = Binarizer(threshold=0.9)
    preds_lstm = scaler_lstm.transform(preds_lstm)

    # save the lstm result to csv 
    resultdata_lstm = pd.DataFrame(preds_lstm)
    resultdata_lstm.to_csv('result_lstm.csv', index=False, header=False, sep=',')

    # calculate the lstm accuracy
    count_lstm = 0
    for i in range(label_length):
        if(preds_lstm[i, 0]==testdata_arlabel[i, 0]):
            count_lstm += 1
    acc_lstm = count_lstm/label_length

##### lstm predict #################################################################################################

    lossdata = [[]]
    # strong accurancy
    count_loss = 0
    for i in range(label_length):
        if(preds_lstm[i, 0]!=preds_rnn[i, 0]):
            # lossdata.append([origiontest.iloc[i, 0:77]])
            count_loss += 1


    return acc_rnn, acc_lstm, count_loss, lossdata
