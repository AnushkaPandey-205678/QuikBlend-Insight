from django.shortcuts import render
import requests
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup as BSoup
from news.models import Headline

# Create your views here.
#import pandas as pd
#from datetime import date
#today = date.today()
##d = today.strftime("%m-%d-%y")
#print("date =" ,d)
#date = 10-1-24

def scrape(request, name):
    Headline.objects.all().delete()
    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url = f"https://www.nbcnews.com/{name}"
    content = requests.get(url).content
    soup = BSoup(content, "html.parser")

    headlines = soup.find_all('div', {'class': 'tease-card__content--inner'})

    for headline in headlines:
        main = headline.find_all("div", class_=True)
        
        title = headline.find("span", {"class": "tease-card__headline"}).text.strip()
        
        link = headline.find("a", {"class": "tease-card__picture-link"})["href"]

        img_tag = headline.find("img")
        img_url = img_tag["src"] if img_tag and "src" in img_tag.attrs else ""

        new_headline = Headline()
        new_headline.title = title
        new_headline.url = link
        new_headline.image = img_url
        new_headline.save()

    return redirect("../")

        # for article in News:
        #   main = article.find_all("a", href=True)
        #
        #  linkx = article.find("a", {"class": "sc-1out364-0 dPMosf js_link"})
        #  link = linkx["href"]

        # 

        # img_tag = article.find("img")
        #  imgx = img_tag["data-src"] if img_tag and "data-src" in img_tag.attrs else "
        #  new_headline.title = title
        #  new_headline.url = link
        #  new_headline.image = imgx
        #  new_headline.save()
    return redirect("../")


def news_list(request):
    headlines = Headline.objects.all()[::-1]
    context = {
        "object_list": headlines,
    }
    return render(request, "news/home.html", context)
