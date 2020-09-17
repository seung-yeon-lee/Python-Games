# 네이버 뉴스 기사 스크래핑
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import quote
import pandas as pd


def get_news(query, page_num=10):
    headers = {'User-Agent': 'Mozilla/5.0'}
    news_df = pd.DataFrame(
        columns=("Title", "Link", "Press", "Datetime", "Article"))
    ids = 0

    url_query = quote(query)
    url = "https://search.naver.com/search.naver?&where=news&sm=nws_hty&query=" + url_query

    for _ in range(0, page_num):
        search_url = urllib.request.Request(url, headers=headers)
        search_data = urllib.request.urlopen(search_url)

        soup = BeautifulSoup(search_data, 'html.parser')
        links = soup.find_all('dd', {'class': 'txt_inline'})

        for link in links:
            press = link.find('span', {'class': '_sp_each_source'}).get_text()
            news_url = link.find('a').get('href')
            if (news_url == '#'):
                continue
            else:
                news_link = urllib.request.urlopen(news_url).read()
                news_html = BeautifulSoup(news_link, 'html.parser')
                title = news_html.find('h3', {'id': 'articleTitle'}).get_text()
                datetime = news_html.find('span', {'class': 't11'}).get_text()
                article = news_html.find(
                    'div', {'id': 'articleBodyContents'}).get_text()

                new_df.loc[idx] = [title, news_url, press, datetime, article]
                idx += 1
                print('#', end="")
        try:
            next = soup.find('a', {'class': 'next'}).get('href')
            url = "https://search.naver.com/search.naver" + next
            print(url)
        except:
            break

    return news_df
