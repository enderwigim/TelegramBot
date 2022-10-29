import requests
from stock import Stock_Machine
from news import NewsRelated
from enterprises import enterprises_dic


class StockView:
    def __init__(self, num):
        self.STOCK = enterprises_dic[num]["stock"]
        self.COMPANY_NAME = enterprises_dic[num]["name"]

        self.my_stock = Stock_Machine(self.STOCK)
        self.my_news = NewsRelated(self.COMPANY_NAME, day1=self.my_stock.day_list[1], day2=self.my_stock.day_list[0])

        self.news_api_url = "https://newsapi.org/v2/everything"
        self.news_api_key = "aa1576800d72490292afe75ae8e76eeb"
        self.news_params = {
            "apiKey": self.news_api_key,
            "q": self.COMPANY_NAME,
            "from": self.my_stock.day_list[1],
            "to": self.my_stock.day_list[0],
            "sortBy": "relevancy",
        }

    def news(self):
        with requests.get(self.news_api_url, params=self.news_params) as response_news:
            response_news.raise_for_status()
            data = response_news.json()
            three_news = data["articles"][:3]
        final_data = [
            {
                "title": three_news[0]['title'],
                "description": three_news[0]['description'],
                "url": three_news[0]['url']
             },
            {
                "title": three_news[1]['title'],
                "description": three_news[1]['description'],
                "url": three_news[1]['url']
            },
            {
                "title": three_news[2]['title'],
                "description": three_news[2]['description'],
                "url": three_news[2]['url']
            }
            ]
        return final_data

    def get_percentage(self):
        messages = []
        percentage = self.my_stock.percentage
        if -1 >= percentage or percentage >= 1:
            # news_data = self.news()
            if percentage >= 1:
                messages += [f"{self.COMPANY_NAME}: 🔺{percentage}%"]
            elif percentage <= -1:
                messages += [f"{self.COMPANY_NAME}: 🔻{percentage}%"]

            messages += [f"Headline: {self.my_news.final_data[0]['title']}\n{self.my_news.final_data[0]['url']}\n"]
            messages += [f"Headline: {self.my_news.final_data[1]['title']}\n{self.my_news.final_data[1]['url']}\n"]
            messages += [f"Headline: {self.my_news.final_data[2]['title']}\n{self.my_news.final_data[2]['url']}\n"]

        else:
            messages += [f"{self.COMPANY_NAME} hasn't seen more than 1% of changes."]
        return messages
