from bs4 import BeautifulSoup
import urllib.request
import pandas as pd


def get_music_ranks(url):
    search_url = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(search_url, 'html.parser')

    soup_titles = soup.select('a._title span.ellipsis')
    titles = [title.get_text() for title in soup_titles]

    soup_artists = soup.select('td._artist.artist > a')
    artists = [artists.get_text().strip() for artists in soup_artists]

    return titles, artists


url_p1 = "https://music.naver.com/listen/top100.nhn?domain=TOTAL_V2&page=1"
titles_50, artists_50 = get_music_ranks(url_p1)


url_p2 = "https://music.naver.com/listen/top100.nhn?domain=TOTAL_V2&page=2"
titles_100, artists_100 = get_music_ranks(url_p2)

ranks = [rank for rank in range(1, 101)]
rank_list = pd.DataFrame({"Rank": ranks,
                          "Title": titles_50 + titles_100,
                          "Artist": artists_50 + artists_100})

rank_list
