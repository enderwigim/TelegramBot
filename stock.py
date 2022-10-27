import requests
import itertools


class Stock_Machine:
    def __init__(self, stock):
        self.alphavantage_url = "https://www.alphavantage.co/query"
        self.alp_key = "5F9HBMIZSU19CY7M"
        self.alp_params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": stock,
            "apikey": self.alp_key
        }
        self.data = self.get_stock()
        self.last_2days = dict(itertools.islice(self.data["Time Series (Daily)"].items(), 2))
        self.day_list = [day for day in self.last_2days]
        self.yesterday_close = float(self.last_2days[self.day_list[0]]["4. close"])
        self.two_days_ago_close = float(self.last_2days[self.day_list[1]]["4. close"])
        self.percentage = round((100 - ((self.yesterday_close / self.two_days_ago_close) * 100)) * -1, 2)

    def get_stock(self):
        with requests.get(self.alphavantage_url, params=self.alp_params) as response:
            response.raise_for_status()
            data = response.json()
            return data




