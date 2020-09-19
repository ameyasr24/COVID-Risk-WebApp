import pandas as pd
from datetime import datetime, date, timedelta

# Get latest COVID-19 data by location using JHU's dataset
yesterday = date.today() - timedelta(days = 1) # use yesterday's data because data is uploaded in the evening
month = '{:02d}'.format(yesterday.month)
day = '{:02d}'.format(yesterday.day)
year = '{:04d}'.format(yesterday.year)

URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/' + str(month) + '-' + str(day) + '-' + str(year) + '.csv'
df = pd.read_csv(URL)
df.dropna(subset = ['Admin2'], inplace = True)

county = input("County: ").title()
state = input("State: ").title()
print(df[(df['Admin2'] == county) & (df['Province_State'] == state)])