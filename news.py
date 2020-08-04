import requests
from bs4 import BeautifulSoup
import json
url = "https://movie.naver.com/movie/running/current.nhn"
req = requests.get(url)
soup = BeautifulSoup(req.text,'html.parser')
movies = soup.select('dt.tit > a')
all_movie= []
for movie in movies:
    movie_info = {'title' : movie.text,
'code' : movie['href'].split('=')[1]}
all_movie.append(movie_info)
print(all_movie)

with open('move_info.json','w', encoding = 'euc-kr') as f:
    json.dump(all_movie, f)