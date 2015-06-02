import pandas as pd
import numpy as np 
# from ggplot import *
import matplotlib.pyplot as plt


weather_df = pd.read_csv("c:\\users\\bonnie\\desktop\\mark_work\\nanodegree\\intro_to_data_science\\improved-dataset\\turnstile_weather_v2.csv")

data = weather_df

# remove Memorial day holiday (30 My 2011) from calculation
test = data[ data['DATEn'] != '05-30-11']
test = test[['day_week', 'ENTRIESn_hourly', 'DATEn']] 
df = test.groupby('day_week', as_index=False)
df1 = df.aggregate(np.mean)


plt.figure()
plt.bar(df1['day_week'], df1['ENTRIESn_hourly']) #, 'ro')
plt.xlabel('Day of the Week')
plt.ylabel('Mean Number of Riders')
plt.xlim([-0.5,7.2])
plt.grid(b=True, which='major', color='grey', alpha=0.5,linestyle='-')
labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
plt.xticks(df1['day_week'] + 0.4, labels)
plt.title("Subway Ridership for May 2011 (Holidays Excluded)")
plt.show()


    
    
