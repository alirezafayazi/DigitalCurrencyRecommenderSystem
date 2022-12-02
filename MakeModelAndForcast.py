import LSTMModel
import VotingReg
from sklearn.preprocessing import MinMaxScaler
import pandas as pd
from sklearn.model_selection import train_test_split
import currences


symbol = currences.symbol
tf=6 #time frame 
def Profit(forcast,close):
    # calculate Price changes in percentage
    profit=((forcast/close)-1)*100
    return profit 

def PreprocessingAndPredict(algorithm):
    percent=[]
    """
    This function prepares the data and predict.
    """
    for i in range(len(symbol)):
        print('predict for :',symbol[i])
        # Load the datas
        data = pd.read_csv(f"./data/{symbol[i]}data.csv")
        usdt=pd.read_csv("./data/USDTdata.csv")
        # Feature selection
        usdt=data.loc[:,['Date','Volume','Market Cap']]
        usdt=usdt.rename(columns={"Volume":"Volume_USDT" ,"Market Cap":"MarketCap_USDT" })
        usdt=usdt.set_index('Date')
        data=data.set_index('Date')
        if len(data)!=len(usdt):# if data length not equal to usdt length:
            usdt=usdt.iloc[0:len(data)]
            
        VolumeUsdt=usdt['Volume_USDT'].tolist()
        MarketCapUsdt=usdt['MarketCap_USDT'].tolist()
        #merge datas
        data['Volume_USDT']=VolumeUsdt
        data['MarketCap_USDT']=MarketCapUsdt

        global t 
        t=data.copy() # t is a copy of data
        
#Build a feature for perdiction (Tomorrow's closing price for per days)
        Close_F=data.Close.iloc[:-1].values 
        data=data.iloc[1:]
        data['Close_F']=Close_F

        data=data.iloc[::-1] # Reverse the data layout
        # Changing the range of data between 0 and 1
        xfit = MinMaxScaler(feature_range = (0, 1)) 
        yfit = MinMaxScaler(feature_range = (0, 1))
        x=xfit.fit_transform(data.drop(['Close_F'],axis=1))
        y=yfit.fit_transform(data['Close_F'].values.reshape(-1, 1))
        if algorithm=='votingreg':
            x=pd.DataFrame(x)
            y=pd.DataFrame(y)
            X_test=pd.DataFrame(xfit.transform(t.iloc[0:2]))
            y_pred=VotingReg.MakeModelAndPredict(x,y,X_test,0.1)
            profit=Profit(yfit.inverse_transform(y_pred)[0][0],t.values[0][3])
            percent.append(profit)
        else :
            print('predict for :',symbol[i])
            X=xfit.transform(t.iloc[0:tf].drop(['Target'],axis=1)) 
            X=X.reshape(1,X.shape[0],X.shape[1])
        # perdict value 
            y_pred=LSTMModel.Pred(X,symbol[i])
            print('Predict for tomorrow :',yfit.inverse_transform(y_pred)[0][0],'Today:',t.values[0][3])
            profit=Profit(yfit.inverse_transform(y_pred)[0][0],t.values[0][3])
            print('predicted profit : ',profit)
            percent.append(profit)
    return percent
    

def PreprocessingAndMakeModel():
    """
    This function prepares the data and trains the model.
    """
    for i in range(len(symbol)):
        print('predict for :',symbol[i])
        print(f'{i+1} :\tMake {symbol[i]} model and save model :')
        # Load the datas
        data = pd.read_csv(f"./data/{symbol[i]}data.csv")
        usdt=pd.read_csv("./data/USDTdata.csv")
        # Feature selection
        usdt=data.loc[:,['Date','Volume','Market Cap']]
        usdt=usdt.rename(columns={"Volume":"Volume_USDT" ,"Market Cap":"MarketCap_USDT" })
        usdt=usdt.set_index('Date')
        data=data.set_index('Date')
        if len(data)!=len(usdt):# if data length not equal to usdt length:
            usdt=usdt.iloc[0:len(data)]
            
        VolumeUsdt=usdt['Volume_USDT'].tolist()
        MarketCapUsdt=usdt['MarketCap_USDT'].tolist()
        #merge datas
        data['Volume_USDT']=VolumeUsdt
        data['MarketCap_USDT']=MarketCapUsdt
        Close_F=data.Close.iloc[:-1].values #Build a feature for perdiction (Tomorrow's closing price for per days)
        data=data.iloc[1:]
        data['Close_F']=Close_F

        data=data.iloc[::-1] # Reverse the data layout
        # Changing the range of data between 0 and 1
        xfit = MinMaxScaler(feature_range = (0, 1)) 
        yfit = MinMaxScaler(feature_range = (0, 1))
        x=xfit.fit_transform(data.drop(['Close_F','Target'],axis=1))
        y=yfit.fit_transform(data['Close_F'].values.reshape(-1, 1))
        # train_test_split
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.1, shuffle=False)
        # change shape of data to fit
        l_test=X_test.shape[0]//tf
        l_train=X_train.shape[0]//tf
        y_train=y_train[0:l_train*tf].reshape(l_train,tf,y_train.shape[1])
        y_test = y_test[0:l_test*tf].reshape(l_test,tf,y_test.shape[1])
        X_train=X_train[0:l_train*tf].reshape(l_train,tf,X_train.shape[1])
        X_test = X_test[0:l_test*tf].reshape(l_test,tf,X_test.shape[1])

        # Fitting the model
        LSTMModel.fit_lstm_model(X_train,y_train ,X_test , y_test,symbol[i])
        print('predict for :',symbol[i])
        
    
   

        
    
