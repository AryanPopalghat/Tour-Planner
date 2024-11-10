import requests

class NewsAgent:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_news_info(self, city, date):
        url = f"https://newsapi.org/v2/everything?q={city}&from={date.strftime('%Y-%m-%d')}&sortBy=popularity&apiKey={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            news_list = [article["title"] for article in articles[:5]]  # Limit to top 5 news articles
            return news_list
        return ["No recent news available."]
