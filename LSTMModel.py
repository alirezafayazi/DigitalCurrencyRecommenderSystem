from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM 
from tensorflow.keras.models import load_model
from sklearn.metrics import r2_score

def fit_lstm_model(X_train,y_train,X_test, y_test, name):
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    # fit model
    model.fit(X_train, y_train, epochs=600, verbose=0)
    # predict
    pred=model.predict(X_test)
    # r2_score
    r2 = r2_score(y_test,pred)
    print(f'** r2_score : { r2*100}\n\n' )
    #save model
    model.save(f'{name}_model.h5')
    
def Pred(X,name):
    global model
    #load model and make predict
    model = load_model(f'./models/{name}_model.h5')
    return model.predict(X)
    
   

    