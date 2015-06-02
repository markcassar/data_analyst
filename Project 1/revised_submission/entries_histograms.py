import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def entries_histogram(turnstile_weather):
    '''
    Before we perform any analysis, it might be useful to take a
    look at the data we're hoping to analyze. More specifically, let's 
    examine the hourly entries in our NYC subway data and determine what
    distribution the data follows. This data is stored in a dataframe
    called turnstile_weather under the ['ENTRIESn_hourly'] column.
    
    Let's plot two histograms on the same axes to show hourly
    entries when raining vs. when not raining. Here's an example on how
    to plot histograms with pandas and matplotlib:
    turnstile_weather['column_to_graph'].hist()
    
    Your histograph may look similar to bar graph in the instructor notes below.
    
    You can read a bit about using matplotlib and pandas to plot histograms here:
    http://pandas.pydata.org/pandas-docs/stable/visualization.html#histograms
    
    You can see the information contained within the turnstile weather data here:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
    '''
    
    plt.figure()
    bins_to_use = list(range(0,34000,1000))
    turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain'] == 0].hist(bins=bins_to_use, log=True,alpha=0.5, align='mid') # your code here to plot a histogram for hourly entries when it is not raining
    turnstile_weather['ENTRIESn_hourly'][turnstile_weather['rain'] == 1].hist(bins=bins_to_use, log=True, alpha=0.7, align='mid') # your code here to plot a histogram for hourly entries when it is raining
    plt.xlabel('Entries per Hour')
    plt.ylabel('Count (logarithmic scale)')
    plt.title(r'Histogram of Entries per Hour')
    plt.xticks(range(0,34000, 2000), rotation='vertical')
    plt.legend( ('not raining', 'raining') )
#    plt.yticks(range(0,18000, 500))
    plt.subplots_adjust(bottom=0.15)


    return plt

if __name__=='__main__':
    df = pd.read_csv("c:\\users\\bonnie\\desktop\\mark_work\\nanodegree\\intro_to_data_science\\improved-dataset\\turnstile_weather_v2.csv")
    entries_histogram(df)
    plt.show()
