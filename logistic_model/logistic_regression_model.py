import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import sklearn.preprocessing as skl_pre
import sklearn.linear_model as skl_lm
import sklearn.discriminant_analysis as skl_da
import sklearn.neighbors as skl_nb
from sklearn.model_selection import GridSearchCV
import sklearn.metrics as skl_met




#DATA PREPROCESSING
data = pd.read_csv('training_data.csv')
data['increase_stock'] = np.where(data['increase_stock'] == 'high_bike_demand', 1, 0)

data.loc[data['month'].isin([12, 1, 2]), 'month'] = 0
data.loc[data['month'].isin([11]) , 'month'] = 1
data.loc[data['month'].isin([3, 5, 7, 8]) , 'month'] = 2
data.loc[data['month'].isin([4, 6, 9, 10]) , 'month'] = 3

data.loc[data['day_of_week'].isin([0,1,2,3,4]), 'day_of_week'] = 0
data.loc[data['day_of_week'].isin([6]), 'day_of_week'] = 1
data.loc[data['day_of_week'].isin([5]), 'day_of_week'] = 2

data.loc[data['hour_of_day'].isin([0, 1, 2, 3, 4, 5, 6, 21, 23]), 'hour_of_day'] = 0
data.loc[data['hour_of_day'].isin([7, 20, 22]), 'hour_of_day'] = 1
data.loc[data['hour_of_day'].isin([8, 9, 10, 11, 12, 13, 14]) , 'hour_of_day'] = 2
data.loc[data['hour_of_day'].isin([15, 16, 19]) , 'hour_of_day'] = 3
data.loc[data['hour_of_day'].isin([17, 18]) , 'hour_of_day'] = 4

data.loc[data['visibility'] < 15, 'visibility'] = True
data.loc[data['visibility'] >= 15, 'visibility'] = False

data.loc[data['snowdepth'] >= 0.01 , 'snowdepth'] = True
data.loc[~(data['snowdepth'] >= 0.01) , 'snowdepth'] = False

data.loc[data['windspeed'] < 30, 'windspeed'] = False
data.loc[data['windspeed'] >= 30, 'windspeed'] = True

data.loc[data['precip'] <=0, 'precip'] = False
data.loc[data['precip'] > 0, 'precip'] = True

data['tempSquare'] = data['temp'] ** 2

data['dewSquare'] = data['dew'] ** 2

data['humiditySquare'] = 1/(data['humidity']**2)

data['badWeather'] = np.empty(len(data.index))
data.loc[(data['snowdepth'] | data['precip'] | data['visibility'] | data['windspeed']), 'badWeather'] = True
data.loc[~(data['snowdepth']  | data['precip'] | data['visibility'] | data['windspeed']) , 'badWeather'] = False


#DATA SPLITING
#keys = ['hour_of_day', 'day_of_week', 'month', 'holiday', 'weekday', 
# 'summertime', 'temp', 'dew', 'humidity', 'precip', 'snow', 'snowdepth',
# 'windspeed', 'cloudcover', 'visibility', 'increase_stock']
np.random.seed(1)
split = 0.8
keys = data.keys()
execlude = ['increase_stock','snow']
features = [x for x in keys if x not in execlude]
train_index = np.random.choice(data.index, size=int(len(data.index) * split), replace=False)
train = data.loc[data.index.isin(train_index)]
test = data.loc[~data.index.isin(train_index)]
train_X, test_X = train[features], test[features] 
train_y, test_y =  np.ravel((train[['increase_stock']]).to_numpy()), np.ravel(test[['increase_stock']].to_numpy()) 

#MODEL CONSTRUCTION
class_weight = {0:1, 1:3}
C= 0.5787
logistic_model = skl_lm.LogisticRegression(solver='lbfgs', max_iter=10000, class_weight=class_weight, C=C)
logistic_model.fit(train_X, train_y)
predict_prob = logistic_model.predict_proba(test_X)
logistic_prediction =np.empty(len(test_y), dtype=object)
logistic_prediction = np.where(predict_prob[:, 0] <0.5, 'high_bike_demand', 'low_bike_demand')

predict_prob = logistic_model.predict_proba(train_X)
logistic_prediction_train =np.empty(len(train_y), dtype=object)
logistic_prediction_train = np.where(predict_prob[:, 0] <0.5, 'high_bike_demand', 'low_bike_demand')


test_y = np.where(test_y == 1, 'high_bike_demand', 'low_bike_demand')
train_y = np.where(train_y == 1, 'high_bike_demand', 'low_bike_demand')

#Confusion Matrix 
print('Confusion Matrices:', "\n")
print("Train LR")
print(pd.crosstab(logistic_prediction_train, train_y), "\n")
print("Test LR")
print(pd.crosstab(logistic_prediction, test_y), "\n")


#Scores
print("\n")
print(f"Train Accuracy LR:{skl_met.accuracy_score(train_y, logistic_prediction_train): .3f}")
print(f"Test Accuracy LR:{skl_met.accuracy_score(test_y, logistic_prediction): .3f}")
print()
print(f"Train recall LR:{skl_met.recall_score(train_y, logistic_prediction_train, pos_label='high_bike_demand'): .3f}")
print(f"Test recall LR:{skl_met.recall_score(test_y, logistic_prediction, pos_label='high_bike_demand'): .3f}")
print()
print(f"Train precision LR:{skl_met.precision_score(train_y, logistic_prediction_train, pos_label='high_bike_demand'): .3f}")
print(f"Test precision LR:{skl_met.precision_score(test_y, logistic_prediction, pos_label='high_bike_demand'): .3f}")
print()
print(f"Train f1 LR:{skl_met.f1_score(train_y, logistic_prediction_train, pos_label='high_bike_demand'): .3f}")
print(f"Test f1 LR:{skl_met.f1_score(test_y, logistic_prediction, pos_label='high_bike_demand'): .3f}")
print()




