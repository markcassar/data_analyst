import numpy as np
import pandas as pd
from ggplot import *
from sklearn import linear_model
import statsmodels.api as sm
import matplotlib.pyplot as plt


'''
Your prediction should have a R^2 value of 0.20 or better.
You need to experiment using various input features contained in the dataframe. 
'''

# read in improved version of the data
dataframe = pd.read_csv("c:\\users\\bonnie\\desktop\\mark_work\\nanodegree\\intro_to_data_science\\project\\turnstile_weather_v2.csv")

# create potential new variables for model
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

# various plots of predictor variables against 'ENTRIESn_hourly' 
ggplot(aes(x='hour', y='ENTRIESn_hourly'), data=dataframe) + geom_point(alpha=0.1)
ggplot(aes(x='hour^2', y='ENTRIESn_hourly'), data=dataframe) + geom_point(alpha=0.1)
ggplot(aes(x='tempi', y='ENTRIESn_hourly'), data=dataframe) + geom_point(alpha=0.1)
ggplot(aes(x='meantempi', y='ENTRIESn_hourly'), data=dataframe) + geom_point(alpha=0.1)
ggplot(aes(x='wspdi', y='ENTRIESn_hourly'), data=dataframe) + geom_point(alpha=0.1)
ggplot(aes(x='meanwspdi', y='ENTRIESn_hourly'), data=dataframe) + geom_point(alpha=0.1)
ggplot(aes(x='pressurei', y='ENTRIESn_hourly'), data=dataframe) + geom_point(alpha=0.1)
ggplot(aes(x='meanpressurei', y='ENTRIESn_hourly'), data=dataframe) + geom_point(alpha=0.1)
ggplot(aes(x='precipi', y='ENTRIESn_hourly'), data=dataframe) + geom_point(alpha=0.1)
ggplot(aes(x='ln(precipi)', y='ENTRIESn_hourly'), data=dataframe) + geom_point(alpha=0.1)
ggplot(aes(x='meanprecipi', y='ENTRIESn_hourly'), data=dataframe) + geom_point(alpha=0.1)
ggplot(aes(x='fog', y='ENTRIESn_hourly'), data=dataframe) + geom_point(alpha=0.1)
ggplot(aes(x='rain', y='ENTRIESn_hourly'), data=dataframe) + geom_point(alpha=0.1)
ggplot(aes(x='hour_tempi', y='ENTRIESn_hourly'), data=dataframe) + geom_point(alpha=0.05)

# example variable transformation to go from quadratic to linear relationship
ggplot(aes(x=[x for x in np.arange(1,10,0.5)], y=[x**2 for x in np.arange(1,10,0.5)]), data=dataframe) + geom_point(alpha=1)
ggplot(aes(x=[x**2 for x in np.arange(1,10,0.5)], y=[x**2 for x in np.arange(1,10,0.5)]), data=dataframe) + geom_point(alpha=1)


