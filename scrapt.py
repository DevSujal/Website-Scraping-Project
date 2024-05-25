import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


url = "http://127.0.0.1:5500/index.html"

data = requests.get(url)

# print(data.text)
soup = BeautifulSoup(data.text, "html.parser")
mydata = pd.DataFrame({"Name": [], "budget": [], "box_office": [], "imdb_rating": []})

s = soup.select(".title")

names = []
budget = []
boxoffice = []
imdb = []
for x in s:
    names.append(x.string)

mydata["Name"] = names

s = soup.find_all("h3")
for value in s:
    text = value.string.split(" ")
    if "budget" in text:
        budget.append(text[text.index(":") + 1])
        continue
    if "Collection" in text:
        boxoffice.append(text[text.index(":") + 1])
        continue
    if "imdb" in text:
        imdb.append(text[text.index(":") + 1])
        continue

mydata["budget"] = budget
mydata["box_office"] = boxoffice
mydata["imdb_rating"] = imdb

mydata.to_csv("moive.csv", index=False)

movie_data = pd.read_csv("moive.csv")

f1 = {"color": "black", "size": 25}
f2 = {"family": "serif", "color": "darkred", "size": 15}

plt.figure(figsize=(11, 5))
plt.bar(movie_data["Name"], movie_data["box_office"], color="g", width=0.5)
plt.title("box office collection of movies", fontdict=f1)
plt.xlabel("Name of movie", fontdict=f2)
plt.ylabel("Box office collection (million dollar)", fontdict=f2)
plt.show()

plt.figure(figsize=(11, 5))
plt.bar(movie_data["Name"], movie_data["imdb_rating"], width=0.5)
plt.title("imdb rating of movies", fontdict=f1)
plt.ylabel("IMDB rating", fontdict=f2)
plt.xlabel("Name of movie", fontdict=f2)
plt.show()

plt.figure(figsize=(10, 15))
f3 = {"family": "serif", "color": "darkred", "size": 15}
i = 0
for i in range(0, len(movie_data["Name"])):
    a = np.array(movie_data.iloc[i][1:3])
    plt.subplot(3, 2, i + 1)
    plt.pie(
        a,
        colors=["red", "limegreen"],
        labels=[
            f"{movie_data.iloc[i][1]} million\n dollar",
            f"{movie_data.iloc[i][2]} million\n dollar",
        ],
    )
    name = f"\n\nbox office collection and\n budget of \n{movie_data.iloc[i][0]}"
    plt.title(name, fontdict=f3)


plt.subplot(3, 2, i + 2)
plt.barh(
    np.array(["Budget", "Box office\ncollection"]),
    np.array([2, 2]),
    color=["red", "limegreen"],
)
plt.show()
