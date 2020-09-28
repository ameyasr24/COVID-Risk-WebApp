import pandas as pd
from datetime import datetime, date, timedelta
import csv

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

casesYesterday = df["Confirmed"][(df['Admin2'] == county) & (df['Province_State'] == state)]

oneWeek = date.today() - timedelta(days = 8) # 7 days from yesterday
month = '{:02d}'.format(oneWeek.month)
day = '{:02d}'.format(oneWeek.day)
year = '{:04d}'.format(oneWeek.year)

URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/' + str(month) + '-' + str(day) + '-' + str(year) + '.csv'
df = pd.read_csv(URL)
df.dropna(subset = ['Admin2'], inplace = True)

casesOneWeek = df[(df['Admin2'] == county) & (df['Province_State'] == state)]


# newCasesOneWeek = float(casesYesterday) - float(casesOneWeek)

county = county + " County"

with open('US_Counties_by_Population.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if row[1] == county:
                if row[2] == state:
                    population = row[3]


# infRateLow = newCasesOneWeek/population
# infRateHigh = infRateLow * 2
