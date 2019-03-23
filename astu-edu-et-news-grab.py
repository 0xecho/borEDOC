import requests
from bs4 import BeautifulSoup as bs

ASTU_NEWS_URL = "http://www.astu.edu.et/latest/news/itemlist/category/1-news?format=feed&type=rss"

resp = requests.get(ASTU_NEWS_URL)

soup = bs(resp.text,"xml")

parsed_data=[]

for i in soup.findAll("item"):
	parsed_data.append([i.title.string,i.link.string,i.description.string,i.author.string,i.pubDate.string])

if __name__ == '__main__':
	print(parsed_data)