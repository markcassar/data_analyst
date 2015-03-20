import numpy as np
import pandas as pd
from ggplot import *
#from sklearn import linear_model
#, svm
#from sklearn.ensemble import RandomForestClassifier
import statsmodels.api as sm
#import itertools
import matplotlib.pyplot as plt
#import operator
#import csv



def normalize_features(df):
    """
    Normalize the features in the data set.
    """
    mu = df.mean()
    sigma = df.std()
    
    if (sigma == 0).any():
        raise Exception("One or more features had the same value for all samples, and thus could " + \
                         "not be normalized. Please do not include features with only a single value " + \
                         "in your model.")
    df_normalized = (df - df.mean()) / df.std()

    return df_normalized, mu, sigma

def compute_cost(features, values, theta):
    """
    Compute the cost function given a set of features / values, 
    and the values for our thetas.
    
    This can be the same code as the compute_cost function in the lesson #3 exercises,
    but feel free to implement your own.
    """
    
    m = len(values)
    sum_of_square_errors = np.square(np.dot(features, theta) - values).sum()
    cost = sum_of_square_errors / (2*m)

    return cost

def gradient_descent(features, values, theta, alpha, num_iterations):
    """
    Perform gradient descent given a data set with an arbitrary number of features.
    """
    
    m = len(values)
    cost_history = []

    for i in range(0, num_iterations):
        cost = compute_cost(features, values, theta)
        cost_history.append(cost)
        h = np.dot( features, theta)
        h_values = values - h 
        theta += (alpha / m) * np.dot( np.transpose(features), h_values )

    return theta, pd.Series(cost_history)
    
def compute_r_squared(data, predictions):
    # Write a function that, given two input numpy arrays, 'data', and 'predictions,'
    # returns the coefficient of determination, R^2, for the model that produced 
    # predictions.

    r_squared = 1 - ( np.sum( np.square(data - predictions) ) / np.sum( np.square( data - np.mean(data) )  ) )

    return r_squared

def predictions(dataframe):
    '''
    The NYC turnstile data is stored in a pandas dataframe called weather_turnstile.
    Using the information stored in the dataframe, let's predict the ridership of
    the NYC subway using linear regression with gradient descent.
    
    You can download the complete turnstile weather dataframe here:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv    
    
    Your prediction should have a R^2 value of 0.20 or better.
    You need to experiment using various input features contained in the dataframe. 
    We recommend that you don't use the EXITSn_hourly feature as an input to the 
    linear model because we cannot use it as a predictor: we cannot use exits 
    counts as a way to predict entry counts. 
    
    '''

    # Select Features (try different features!)

#    feature_lst = [  'fog','pressurei', 'meanpressurei', 'tempi', 'wspdi', 'precipi', 'rain', 'meantempi', 'latitude', 'longitude', 'meanwspdi', 'meanprecipi', 'hour']
    feature_lst = [  'fog','pressurei', 'tempi', 'wspdi', 'precipi', 'rain', 'meantempi', 'meanwspdi', 'meanprecipi', 'hour']
    
    features = dataframe[ feature_lst ]

    # Add features using dummy variables
    dummy_units = pd.get_dummies(dataframe['UNIT'], prefix='unit')
    dummy_day_week = pd.get_dummies(dataframe['day_week'], prefix='day')
#    dummy_station = pd.get_dummies(dataframe['station'], prefix='station')
    dummy_conds = pd.get_dummies(dataframe['conds'], prefix='conds')
    features = features.join(dummy_units)
    features = features.join(dummy_day_week)
#    features = features.join(dummy_station)
    features = features.join(dummy_conds)
    
    # Values
    values = dataframe['ENTRIESn_hourly']
    m = len(values)

    features, mu, sigma = normalize_features(features)
    features['ones'] = np.ones(m) # Add a column of 1s (y intercept)
    
    # Convert features and values to numpy arrays
    features_array = np.array( features)
    values_array = np.array(values)

# this model works
#    clf = linear_model.LinearRegression()
#    results = clf.fit(features_array, values_array)
#    prediction = results.predict(features_array)

# this model does not yet work
#    model = RandomForestClassifier()
#    y, _ = pd.factorize(dataframe['ENTRIESn_hourly'])
#    results = model.fit(features_array, values_array)
#    prediction = model.predict(features_array)

# this model takes too long to calculate, if indeed it does actually calculate the predictions properly (I didn't wait for it to finish)
#    model = svm.SVR(kernel='linear', C=1e3)
#    results = model.fit(features_array, values_array.astype(np.float))
#    prediction = results.predict(features_array)
    

    model = sm.OLS(values_array, features_array)
    results = model.fit()    
    prediction = results.predict(features_array)

    print( compute_r_squared(values, prediction) )
#    print(results.summary())
    
    plt.scatter(values_array, prediction-values_array)
#    plt.xticks(range(len(feature_r_squared_dict)), feature_r_squared_dict.keys(), rotation='vertical')
    plt.show()

    
    return prediction #, plot


def plot_cost_history(alpha, cost_history):
   """This function is for viewing the plot of your cost history.
   
   If you want to run this locally, you should print the return value
   from this function.
   """
   cost_df = pd.DataFrame({
      'Cost_History': cost_history,
      'Iteration': range(len(cost_history))
   })
   return ggplot(cost_df, aes('Iteration', 'Cost_History')) + \
      geom_point() + ggtitle('Cost History for alpha = %.3f' % alpha )
      
      
if __name__=='__main__':
    df = pd.read_csv("c:\\users\\bonnie\\desktop\\mark_work\\nanodegree\\intro_to_data_science\\improved-dataset\\turnstile_weather_v2.csv")

    predictions(df)

    
    