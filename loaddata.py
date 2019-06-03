import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import Normalizer

def LoadTrainData():
    # read in csv data using pandas
    data_mon = pd.read_csv('/home/uscc/Ncsis_Docker_IDS/TrafficLabelling /Monday-WorkingHours.csv')
    data_tue = pd.read_csv('/home/uscc/Ncsis_Docker_IDS/TrafficLabelling //Tuesday-WorkingHours.csv')
    data_wed = pd.read_csv('/home/uscc/Ncsis_Docker_IDS/TrafficLabelling /Wednesday-workingHours.csv')
    data_thu1 = pd.read_csv('/home/uscc/Ncsis_Docker_IDS/TrafficLabelling /Thursday-WorkingHours-Morning-WebAttacks.csv')
    data_thu2 = pd.read_csv('/home/uscc/Ncsis_Docker_IDS/TrafficLabelling /Thursday-WorkingHours-Afternoon-Infilteration.csv')
    data_fri1 = pd.read_csv('/home/uscc/Ncsis_Docker_IDS/TrafficLabelling /Friday-WorkingHours-Morning.csv')
    data_fri2 = pd.read_csv('/home/uscc/Ncsis_Docker_IDS/TrafficLabelling /Friday-WorkingHours-Afternoon-DDos.csv')
    data_fri3 = pd.read_csv('/home/uscc/Ncsis_Docker_IDS/TrafficLabelling //Friday-WorkingHours-Afternoon-PortScan.csv')

    # concatenate all dataset
    data = pd.concat([data_mon, data_tue, data_wed, data_thu1, data_thu2, data_fri1, data_fri2, data_fri3], axis=0, ignore_index=True)

    # replace string to int on ' Label'
    relabel = data[' Label'].copy()
    relabel[relabel != 'BENIGN'] = 0
    relabel[relabel == 'BENIGN'] = 1
    data[' Label'] = relabel

    # # replace string to int on 'Flow Bytes/s'
    # reflowbytes = data['Flow Bytes/s'].copy()
    # reflowbytes[reflowbytes == 'NaN'] = 0
    # reflowbytes[reflowbytes == 'Infinity'] = 0
    # data['Flow Bytes/s'] = reflowbytes

    # # replace string to int on ' Flow Packets/s'
    # reflowpackets = data[' Flow Packets/s'].copy()
    # reflowpackets[reflowpackets == 'Infinity'] = 0
    # data[' Flow Packets/s']  = reflowpackets

    # delete columns which has string value
    data = data.drop(['Flow ID', ' Source IP', ' Destination IP', ' Timestamp', 'Flow Bytes/s', ' Flow Packets/s'], axis = 1)

    # # store the dataframe to csv file
    # data.to_csv('all.csv', index=True, header=True, sep=',')


    # segment data to train data & test data & valid data
    traindata = data.sample(frac=0.9, random_state=7)
    testdata = data.loc[~data.index.isin(traindata.index)]
    validdata = traindata.sample(frac=0.1, random_state=17)

    # create a dataframe with all training data & testing data & valid data except the target column 
    traindata_X = traindata.iloc[:, 0:77]
    traindata_Y = traindata.iloc[:, 78]
    testdata_X = testdata.iloc[:, 0:77]
    testdata_Y = testdata.iloc[:, 78]
    validdata_X = validdata.iloc[:, 0:77]
    validdata_Y = validdata.iloc[:, 78]

    # # convert *_X to float64
    # traindata_X = traindata_X.astype(np.float64)
    # testdata_X = testdata_X.astype(np.float64)
    # validdata_X = validdata_X.astype(np.float64)

    # # convert *_Y to float64
    # traindata_Y = traindata_Y.astype(np.int)
    # testdata_Y = testdata_Y.astype(np.int)
    # validdata_Y = validdata_Y.astype(np.int)

    # normalize the data & convert dataframe to numpy array
    scaler = Normalizer().fit(traindata_X)
    traindata_X = scaler.transform(traindata_X)
    np.set_printoptions(precision=3)

    scaler = Normalizer().fit(testdata_X)
    testdata_X = scaler.transform(testdata_X)
    np.set_printoptions(precision=3)

    scaler = Normalizer().fit(validdata_X)
    validdata_X = scaler.transform(validdata_X)
    np.set_printoptions(precision=3)

    # convert dataframe to numpy array
    traindata_arY = np.array(traindata_Y)
    testdata_arY = np.array(testdata_Y)
    validdata_arY = np.array(validdata_Y)

    # reshape input to be [samples, time steps, features]
    traindata_arX = np.reshape(traindata_X, (traindata_X.shape[0], 1, traindata_X.shape[1]))
    testdata_arX = np.reshape(testdata_X, (testdata_X.shape[0], 1, testdata_X.shape[1]))
    validdata_arX = np.reshape(validdata_X, (validdata_X.shape[0], 1, validdata_X.shape[1]))
    
    return traindata_arX, traindata_arY, testdata_arX, testdata_arY, validdata_arX, validdata_arY
    
