# scrape all genres off of http://everynoise.com/everynoise1d.cgi?scope=all

import requests
from bs4 import BeautifulSoup
import csv

# website = requests.get("http://everynoise.com/everynoise1d.cgi?scope=all")
# source = website.text

# now we need to scrape the source file for the information we need, use beautiful soup for that to first make it readable
with open("genreList.html", "r") as genreList:
    soup = BeautifulSoup(genreList.read(), 'lxml')
    print(soup.prettify())

    temp = list(soup.find_all("a", {"title": 'Re-sort the list starting from here.'}))
    output = [tempy.string for tempy in temp]

    with open("genreList.csv", "w") as fout:
        csv_writer = csv.writer(fout)
        csv_writer.writerow(output)
