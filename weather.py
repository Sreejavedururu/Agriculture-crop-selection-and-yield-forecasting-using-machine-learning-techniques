import requests


class Weather():

    def __init__(self, config):
        self.location = None
        self.config = config

    def set_location(self, location):
        self.location = location

    def get_location(self):
        return self.location

    def download_weather_data(self):
        params = {
            'q': self.location,
            'appid': self.config['API_KEY'],
            'units': 'metric'
        }
        try:
            response = requests.get(self.config['API_URL'], params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError:
            raise WeatherException("Weather for {} not found".format(self.location))

    def get_forecast_data(self):
        weather = self.download_weather_data()
        w = weather['list']
        current = w[0]['weather'][0]['description'], w[0]['main']['temp']
        tomorrow = w[1]['weather'][0]['description'], w[1]['main']['temp']
        dayafter = w[2]['weather'][0]['description'], w[2]['main']['temp']
        Next = w[3]['weather'][0]['description'], w[3]['main']['temp']
        return weather['city']['name'], current, tomorrow, dayafter, Next


class WeatherException(Exception):

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        if self.message:
            return self.message
        else:
            return "Weather not found!"
