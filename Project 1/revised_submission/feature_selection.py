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

# create new variables for possible exploration in model
dataframe['hour^2'] = dataframe['hour']**2
dataframe['hour^3'] = dataframe['hour']**3
dataframe['log2(hour)'] = np.log2(dataframe['hour'].astype(float)+1)
dataframe['ln(hour)'] = np.log1p(dataframe['hour'].astype(float))
dataframe['log10(hour)'] = np.log10(dataframe['hour'].astype(float)+1)
dataframe['tempi^2'] = dataframe['tempi']**2
dataframe['tempi^3'] = dataframe['tempi']**3
dataframe['log2(tempi)'] = np.log2(dataframe['tempi'].astype(float)+1)
dataframe['ln(tempi)'] = np.log1p(dataframe['tempi'].astype(float))
dataframe['log10(tempi)'] = np.log10(dataframe['tempi'].astype(float)+1)
dataframe['ln(precipi)'] = np.log1p(dataframe['precipi'].astype(float))
dataframe['hour_tempi'] = dataframe['hour'] * dataframe['tempi']

# Select Features (try different features!)
# list of all available features from the dataset
# exclude latitude and longitude as they consistently introduce very large coefficients
feature_lst = [ 'hour^2', 'hour^3', 'fog','pressurei', 'meanpressurei', 'tempi', 'wspdi', 'precipi', 'rain', 'meantempi', 'meanwspdi', 'meanprecipi']

# list of features as added, one by one, based on R^2 value and coefficients
features_chosen = ['hour'] #'meantempi'] 

new_feature_lst = list(set(feature_lst) - set(features_chosen))

# create empty dictionaries to hold R^2 values and coefficients as we test new features in the subsequent loop
feature_R2 = {}
feature_coef = {}

# a loop to test feature by feature as we build our model
for feature in new_feature_lst:
    feature_select = [feature]
    feature_select = feature_select + features_chosen
    print "Checking ", feature_select, " now!"
    features = dataframe[ feature_select ]

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
    
    #print features.columns.values

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
    
    # capture the coefficients and the R^2 value
    feature_coef[feature] = regr.coef_
    feature_R2[feature] = regr.score(features_array, values)
    

#  plot of predicted value against difference between actual and predicted value, also known as residuals
plt.scatter(prediction, values_array - prediction, alpha=0.05)
plt.show()


#various histograms of possible interest
x_hist = pd.DataFrame(values_array - prediction)
x_hist.columns = ['residuals']
x_hist['predictions'] = prediction
x_hist['values'] = values_array
x_hist['variance*n'] = dataframe['ENTRIESn_hourly'] - np.mean( dataframe['ENTRIESn_hourly'] )
ggplot(aes(x='residuals'), data=x_hist) + geom_histogram(binwidth=100)
ggplot(aes(x='variance*n'), data=x_hist) + geom_histogram(binwidth=100)
ggplot(aes(x='predictions'), data=x_hist) + geom_histogram(binwidth=100)
ggplot(aes(x='values'), data=x_hist) + geom_histogram(binwidth=100)


print np.var(dataframe['ENTRIESn_hourly'])
print np.sum(values_array - prediction)
print mean_squared_error(values_array, prediction)

min(values_array)
max(values_array)
min(prediction)
max(prediction) 
   
def keywithmaxval(d):
     """ a) create a list of the dict's keys and values; 
         b) return the key with the max value"""  
     v=list(d.values())
     k=list(d.keys())
     return k[v.index(max(v))], max(v)

print     
print "Key with maximum R^2 value is: {0}".format(keywithmaxval(feature_R2))
maxkey = keywithmaxval(feature_R2)[0]

print "Maximum absolute value of coefficients is: {0}".format(max(abs(feature_coef[maxkey])))

   