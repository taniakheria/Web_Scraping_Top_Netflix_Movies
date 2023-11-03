import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://editorial.rottentomatoes.com/guide/best-netflix-movies-to-watch-right-now/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
}
result = requests.get(url)
htmlContent = result.text

soup = BeautifulSoup(htmlContent, 'html.parser')
# print(soup.prettify())

movie_data = []

# Web Scraping 
movies = soup.findAll("div", class_="row countdown-item")
for movie in movies:
    movie_name = movie.find("div", class_="article_movie_title").find('a').text
    movie_link = movie.find("div", class_="article_movie_title").find('a')['href']
    rating = movie.find("span", class_="tMeterScore").text
    # print(rating)
    director = movie.find(class_="info director").find('a').text
    cast = movie.find(class_="info cast").findAll('a')
    cast_names = []
    for a in cast:
      cast_names.append(a.text)
    # print(cast_names) 
    movie_details = {
       "Name" : movie_name,
       "Link" : movie_link,
       "Rating" : rating,
       "Director" : director,
       "Cast" : cast_names
    }
    movie_data.append(movie_details)

df = pd.DataFrame(movie_data)

# Changing the data type of Cast column to String 
df['Cast'] = df['Cast'].astype(str)

# Assuming df is your DataFrame
df['Cast'] = df['Cast'].str.strip('[]').str.replace("'", "")

# Saving the file 
file_path = "D:\PROGRAMMING PROJECTS\Movies.xlsx"
df.to_excel(file_path, index=False)

