import requests

class NewsRelated:
    def __init__(self, company_name, day2, day1):
        self.news_api_url = "https://newsapi.org/v2/everything"
        self.news_api_key = "aa1576800d72490292afe75ae8e76eeb"
        self.news_params = {
            "apiKey": self.news_api_key,
            "qInTitle": company_name,
            "from": day2,
            "to": day1,
            "sortBy": "relevancy",
        }
        self.final_data = self.news()

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
