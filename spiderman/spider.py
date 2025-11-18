import requests
from bs4 import BeautifulSoup
import time
import csv

def douban_movie_spider():
    headers = {"user-agent":
                   "Mozilla/5.0 "
                   "(Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 "
                   "(KHTML, like Gecko) "
                   "Chrome/134.0.0.0 Safari/537.36"
               }
    base_url = "http://movie.douban.com/top250"

    movies = []

    for i in range(0,2):
        full_url = f"{base_url}?start={i*25}"
        response = requests.get(full_url,headers=headers)

        soup = BeautifulSoup(response.text,"html.parser")

        movie_items = soup.find_all("div",class_="item")
        for movie in movie_items:
            movie_title = movie.find("span",class_="title").text
            movie_link = movie.find("a").get("href")
            rating_num = movie.find("span",class_="rating_num").text

            movieinfo = {"name":movie_title,"rating_num":rating_num,"link":movie_link}

            movies.append(movieinfo)

        time.sleep(5)

    return movies

for movie in douban_movie_spider():
    print(movie)
    print("-" * 50)
def save_csv(movies):
    with open("movies.csv","w",newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["电影名称","评分","链接"])

        for movie in movies:
            writer.writerow([movie["name"],movie["rating_num"],movie["link"]])


def main():
    movies = douban_movie_spider()
    save_csv(movies)
#
# if __name__ == "__main__":
#     main()














