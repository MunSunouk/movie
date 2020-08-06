import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud

def create_word_cloud(replies):
    movie_mask = np.array(Image.open('./movie_image.jpg'))
    cloud = WordCloud(background_color = 'white', mask = movie_mask)
    movie_cloud = cloud.fit_words(replies)
    cloud.to_file('cloud_moive.png')
    return movie_cloud


response = requests.get('https://movie.naver.com/movie/running/current.nhn')
soup = BeautifulSoup(response.text, 'html.parser')

movies_list = soup.select(
    '#content > .article > .obj_section > .lst_wrap > ul > li')

final_movie_data = []

for movie in movies_list:
    a_tag = movie.select_one('dl > dt > a')

    movie_title = a_tag.contents[0]
    movie_code = a_tag['href'].split('code=')[1]
    
    movie_data = {
        'title': movie_title,
        'code': movie_code
    }

    final_movie_data.append(movie_data)
for title,code in final_movie_data:
    url = f'https://movie.naver.com/movie/bi/mi/basic.nhn?code={code}'
    headers = {
    'authority': 'movie.naver.com',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'iframe',
    'referer': f'https://movie.naver.com/movie/bi/mi/point.nhn?code={code}',
    'accept-language': 'en-US,en;q=0.9,ko;q=0.8',
    'cookie': 'NNB=CXMBCTM3ZHQF4; NRTK=ag^#all_gr^#1_ma^#-2_si^#0_en^#0_sp^#0; NM_THUMB_PROMOTION_BLOCK=Y; csrf_token=e45745b0-db53-434c-81f6-2e5336a2f59e',
    }
    req = requests.get(url,headers = headers)
    soup = BeautifulSoup(req.text,"html.parser")

    result = []
    replies = []

    box = soup.find("div",class_ = "score_result")
    score = box.find("div", class_ = "star_score").find("em").get_text()
    replies.append([score])
    for reple in box.find_all("div",class_ = "score_reple"):
        result.append(reple.find("p").get_text())
        for sentence in result:
            sentence = sentence.replace('\t','').replace('\n','')
            words = sentence.split()
            for word in words:
                replies.append(word)
    print(replies)
    replies = Counter(replies)
    print(create_word_cloud(replies))