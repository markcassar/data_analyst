import pandas as pd
import numpy as np 
from ggplot import *
import matplotlib.pyplot as plt


def plot_weather_data(turnstile_weather):
    '''
    You are passed in a dataframe called turnstile_weather. 
    Use turnstile_weather along with ggplot to make a data visualization
    focused on the MTA and weather data we used in assignment #3.  
    You should feel free to implement something that we discussed in class 
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.  

    You can check out:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
     
    To see all the columns and data points included in the turnstile_weather 
    dataframe. 
     '''

    data = turnstile_weather
    
    df_rain = data[ data['rain'] == 1 ]
    df_no_rain = data[ data['rain'] == 0 ]
    df_rain1 = df_rain.apply(np.sum)
    df_no_rain1 = df_no_rain.apply(np.sum)
    print(df_rain1['ENTRIESn_hourly'])
    print(df_no_rain1['ENTRIESn_hourly'])

    df = data.groupby('day_week', as_index=False)
#    df = data.groupby('tempi', as_index=False)
    df1 = df.aggregate(np.sum)
    

    plt.figure()
    plt.plot(df1['day_week'], df1['ENTRIESn_hourly'], 'ro')
    plt.xlabel('Day of the Week')
    plt.ylabel('Entries per Hour')
    plt.xlim([-1,7])
    plt.ylim([0,1.6e7])
    plt.grid(b=True, which='major', color='grey', alpha=0.5,linestyle='-')
    labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    plt.xticks(df1['day_week'], labels)
    plt.title("Subway Ridership by Day of the Week")
    plt.show()


if __name__ == "__main__":
    weather_df = pd.read_csv("c:\\users\\bonnie\\desktop\\mark_work\\nanodegree\\intro_to_data_science\\improved-dataset\\turnstile_weather_v2.csv")
    plot_weather_data(weather_df)
    
    
