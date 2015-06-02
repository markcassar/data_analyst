

weather_data = read.csv("c:\\users\\bonnie\\desktop\\mark_work\\nanodegree\\intro_to_data_science\\project\\turnstile_weather_v2.csv")

entries_no_rain <- weather_data$ENTRIESn_hourly[weather_data$rain == 0]
entries_rain <- weather_data$ENTRIESn_hourly[weather_data$rain == 1]

no_rain_mean = mean(weather_data$ENTRIESn_hourly[weather_data$rain == 0])
rain_mean = mean(weather_data$ENTRIESn_hourly[weather_data$rain == 1])  

results <- wilcox.test(entries_no_rain, entries_rain)
