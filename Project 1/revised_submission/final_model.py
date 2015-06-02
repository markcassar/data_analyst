import numpy as np
import pandas as pd
from ggplot import *
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
#import statsmodels.api as sm
import matplotlib.pyplot as plt


'''
Your prediction should have a R^2 value of 0.20 or better.
You need to experiment using various input features contained in the dataframe. 
'''

# read in improved dataset
dataframe = pd.read_csv("c:\\users\\bonnie\\desktop\\mark_work\\nanodegree\\intro_to_data_science\\project\\turnstile_weather_v2.csv")

# Selected Features 
feature_lst = [ 'hour', 'tempi', 'meantempi']

features = dataframe[ feature_lst ]

# Add features using dummy variables
# using dummy variables based on the 'UNIT' variable produced the best results
dummy_units = pd.get_dummies(dataframe['UNIT'], prefix='unit')
dummy_day_week = pd.get_dummies(dataframe['day_week'], prefix='day')
#dummy_station = pd.get_dummies(dataframe['station'], prefix='station')
dummy_conds = pd.get_dummies(dataframe['conds'], prefix='conds')

features = features.join(dummy_units)
features = features.join(dummy_day_week)
#features = features.join(dummy_station)
features = features.join(dummy_conds)

# remove one of each of the dummy variables as it is not independent of the others,  
#     e.g., if the dummy variables were based on gender, we do not need to include both 'male' and 'female' 
#       as dummy variables as a '0' in the female column is identical to a '1' in the male column
#del features['UNIT']
del features['unit_R464']
#del features['day_week']
del features['day_6']
#del features['conds']
del features['conds_Scattered Clouds']
#del features['station']
#del features['station_WORLD TRADE CTR']

# target values
values = dataframe['ENTRIESn_hourly']

# Convert features and values to numpy arrays
features_array = np.array( features)
values_array = np.array(values)

# using scikit learn's linear regression method
# normalize set to True so that features are normalized before regression is done
regr = linear_model.LinearRegression(fit_intercept=True, normalize=True)
results = regr.fit(features_array, values_array)
prediction = results.predict(features_array) #+ abs(regr.intercept_)

print "The first 10 coefficients of the model are:\n {0}".format(regr.coef_[0:10])
print
print "Maximum (absolute value) coefficient is: {0}".format(max(abs(regr.coef_)))
print
print "Model intercept is: {0}".format(regr.intercept_)
print
print "Total number of features in the model is: {0}".format( len( regr.coef_ ) + 1 )
print
print "Non-dummy features of the model are: {0}".format( feature_lst)
print
print "Model R^2 is: {0}".format( regr.score(features_array, values) )
 
    

#  plot of predicted value against difference between actual and predicted value, also known as residuals
#plt.scatter(prediction, values_array - prediction, alpha=0.05)
#plt.show()


#print np.var(dataframe['ENTRIESn_hourly'])
#print np.sum(values_array - prediction)
#print mean_squared_error(values_array, prediction)
#
#min(values_array)
#max(values_array)
#min(prediction)
#max(prediction) 
   



   