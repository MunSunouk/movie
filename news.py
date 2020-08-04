import requests
from bs4 import BeautifulSoup

url = "https://movie.naver.com/movie/running/current.nhn"
req = requests.get(url)
soup = BeautifulSoup(req,html.parser)
movies = soup.select('.tit > a')
all_movie= []
for movie in movies:
    movie_info = {'title' : movie.text,
'code' : movie['href'].split('=')[1]}
all_movie.append(movie_info)
print(all_movie)

