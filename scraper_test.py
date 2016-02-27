__author__ = 'Dempw'

from scraper import scrape_weather_data_on_interval
import datetime

print 'Date\t\tT\tRain\tPressure'

start = datetime.date(2016, 2, 1)
end = datetime.datetime.now()
wd = scrape_weather_data_on_interval(start, end)

for data in wd:
    print data

# Single date data scraping test

# from scraper import scrape_weather_data_on_date
# start = datetime.date(2016, 2, 20)
# wd = scrape_weather_data_on_date(start)
# print wd


