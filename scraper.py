__author__ = 'Dempw'

from lxml import html
import requests
import datetime


class WeatherData:
    def __init__(self, date, temperature, rain, pressure, events):
        self.date = date
        self.temperature = temperature
        self.rain = rain
        self.pressure = pressure
        self.events = events

    def __str__(self):
        data = self.date.strftime('%Y/%m/%d/') + '\t' + str(self.temperature) +\
             '\t' + str(self.rain) + '\t' + str(self.pressure) + '\t' + str(self.events)
        return data


def scrape_weather_data_on_date(date):
    url_date = date.strftime('%Y/%m/%d/')
    url = 'https://www.wunderground.com/history/airport/EPWR/' + \
          url_date + 'DailyHistory.html'

    page = requests.get(url)
    tree = html.fromstring(page.content)

    # Average day temperature is located in the first span
    # and needs conversion from Fahrenheit to Celsius
    temperature = tree.xpath('(//span[@class="wx-value"])[1]/text()').pop()
    temperature = int((int(temperature) - 32) / 1.8)

    # There is a problem with indexing html DOM structure
    # (index 8 -> 6 and 10 -> 8), which is messy and
    # incoherent
    #
    # # Average day rainfall is given on inches, so it needs
    # # a conversion to mm
    rain = tree.xpath("(//span[contains(.,'Precipitation')]/"
                      "parent::td/following-sibling::td)[1]//"
                      "span[@class='wx-value']/text()").pop()
    rain = float(rain) * 25.4
    #
    # # Pressure is given in inches, so it needs a conversion
    # # to hPa
    pressure = tree.xpath("(//span[contains(.,'Pressure')]/"
                          "parent::td/following-sibling::td)[1]//"
                          "span[@class='wx-value']/text()").pop()
    pressure = float(pressure) * 33.86

    # Temporarily events are in form of regular strings.                XXX
    # Will be changed to enum or class after analysis
    events = tree.xpath("(//span[contains(.,'Events')]/"
                        "parent::td/following-sibling::td)[1]/"
                        "text()").pop().replace("\n", "").replace("\t", "")\
                        .encode("ascii", "ignore")

    return WeatherData(date, temperature, rain, pressure, events)


def scrape_weather_data_on_interval(start_date, end_date):
    result = []
    date = start_date

    # We can't go beyond now
    while date < end_date.date() and date < datetime.datetime.now().date():

        # XXX crawl_weather_data_on_date may produce errors
        weather_data = scrape_weather_data_on_date(date)

        # Print is temporary, just for presentation purpose
        # result.append(weather_data)
        print weather_data

        # Step up to the next day
        date = date + datetime.timedelta(1)

    return result
