from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import VotingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

def MakeModelAndPredict(X,y,Xtest,t=0.1,shu=False):
    # train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=t, shuffle=shu)
    # change shape 
    y_train=np.ravel(y_train.values)
    y_test=np.ravel(y_test.values)
    X_test = X_test.values
    X_train=X_train.values

    reg1 = GradientBoostingRegressor()
    reg2 = RandomForestRegressor()
    reg3 = LinearRegression()

    reg1.fit(X_train, y_train)
    reg2.fit(X_train, y_train)
    reg3.fit(X_train, y_train)

    ereg = VotingRegressor(estimators=[('gb', reg1), ('rf', reg2), ('lr', reg3)])
    ereg = ereg.fit(X_train, y_train)
    pred = ereg.predict(X_test)

    r2 = r2_score(y_test,pred)
    print(f'** r2_score : { r2*100}\n\n' )
    pred = pd.DataFrame(ereg.predict(Xtest), index=Xtest.index, columns=y.columns)
    return pred