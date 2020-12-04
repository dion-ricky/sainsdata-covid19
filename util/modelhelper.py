from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from joblib import dump as jldump
import math

# Class ModelRepository
class ModelRepository:
    
    def __init__(self, X_train, X_test, y_train, y_test, y_pred, regr_model):
        self.__X_train = X_train
        self.__X_test = X_test
        self.__y_train = y_train
        self.__y_test = y_test
        self.__y_pred = y_pred
        self.__regr = regr_model
        
    def r2_score(self):
        return r2_score(
            self.__y_test, self.__y_pred
        )
        
    def predict(self, i):
        return self.__regr.predict(i)
    
    def get_X_train(self):
        return self.__X_train
    
    def get_X_test(self):
        return self.__X_test
    
    def get_y_train(self):
        return self.__y_train
    
    def get_y_test(self):
        return self.__y_test
    
    def get_model(self):
        return self.__regr
    
    def dump(self, fn):
        return jldump(self, fn)

def get_model_above_threshold(X, y, r2_threshold, test_size=None):
    while True:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)
        _regr = LinearRegression()

        _regr.fit(X_train, y_train)

        y_pred = _regr.predict(X_test)

        _r2_score = r2_score(y_test, y_pred)

        if _r2_score < r2_threshold:
            continue

        return ModelRepository(X_train, X_test, y_train, y_test, y_pred, _regr)





