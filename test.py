import numpy as np 
import pandas as pd

from  keras.models import Sequential, load_model
from sklearn.preprocessing import Normalizer, Binarizer

def test(cvefile_path):

##### testdata preprocessing #######################################################################################
    # read in csv data using pandas
    testdata = pd.read_csv(cvefile_path)

#     reflowpackets = testdata[' Flow Packets/s'].copy()
#     reflowpackets[reflowpackets == 'Infinity'] = 0
#     testdata[' Flow Packets/s']  = reflowpackets

    # delete columns which has string value
    testdata = testdata.drop(['Flow ID', 'Src IP', 'Dst IP', 'Timestamp', 'Flow Byts/s', 'Flow Pkts/s', 'Label'], axis = 1)

    # create a dataframe with testing data & testing label 
    testdata = testdata.iloc[:, 0:77]
    origiontest = testdata

    # normalize the data & convert dataframe to numpy array
    scaler = Normalizer().fit(testdata)
    testdata = scaler.transform(testdata)
    np.set_printoptions(precision=3)

    # reshape input to be [samples, time steps, features]
    testdata_length = testdata.shape[0]
    testdata_ar = np.reshape(testdata, (testdata.shape[0], 1, testdata.shape[1]))

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

##### lstm predict #################################################################################################

    weak_dangerflow = []
    strong_dangerflow = []
    safe_flow = []

    for i in range(testdata_length):
        if(preds_lstm[i, 0]!=preds_rnn[i, 0]):
            weak_dangerflow.append([origiontest.iloc[i, 0:77]])
        elif(preds_lstm[i, 0]==preds_rnn[i, 0]==0):
            weak_dangerflow.append([origiontest.iloc[i, 0:77]])
        elif(preds_lstm[i, 0]==preds_rnn[i, 0]==1):
            safe_flow.append([origiontest.iloc[i, 0:77]])

    return  safe_flow, weak_dangerflow, strong_dangerflow


