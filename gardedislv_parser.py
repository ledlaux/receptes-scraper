#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as Ureq

url = 'http://gardedis.lv/'

# Gets recipe categories url
def recipe_category(url):
    category_list = []
    uClient = Ureq(url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "lxml")
    categories = []
    for links in page_soup.find_all('ul', {'class': 'alx-nav-pills'}):
        for li in links.find_all('li'):
            categories.append(li)
    for category_name in categories:
        print(category_name.find('a')['href'])


# Put here any category adress from previous function
category_url = "/category/saldie-edieni/"

def recipe_url(category_url):
    url_list = []
    pagination_url = []
    for x in range(1, 4):      # Takes long time to process, you can change the range.
        pagination_url.append("http://gardedis.lv"+ category_url + "?page=" + str(x))
    for url in pagination_url:
        try:
            uClient = Ureq(url)
            page_html = uClient.read()
            uClient.close()
            page_soup = soup(page_html, "html.parser")
            links = page_soup.findAll('h2', class_='post-title')
        except:
            break
        for div in links:
            url_list.append(div.find('a')['href'])
    recipes_list = []
    for recipe in url_list:
        recipes_list.append('http://gardedis.lv' + recipe)
    for adress in recipes_list:
        print(adress)

adress = "" # Put here recipe url from previous function

# Parse recipe description and image
def gardedis_parser(adress):
    uClient = Ureq(adress)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")

    title = page_soup.find('h1', class_='post-title')

    images = page_soup.find("div", {"class": "post-thumbnail"})
    image = images.find('img')['src']

    ingredients_list = []
    ingredients = page_soup.find('div', class_='grid two-fifth')
    i = ingredients.text.strip()
    ingredients_fix = i.replace(u'\xa0', u' ')
    fix = ingredients_fix.replace(u'\n', u' ')
    ingredients_list.append(fix)

    cooking = page_soup.find(
        'div', class_='grid three-fifth last').getText().strip()
    cooking_fix = cooking.replace(u'Pagatavošana', u' ')

    print(title.getText())
    for x in ingredients_list:
        print(x)
    print('Pagatavošana:')
    print(cooking_fix.strip())
    if image:
        try:
            print(image)
        except:
            pass


if __name__ == "__main__":
    recipe_category(url)
    recipe_url(category_url)
    gardedis_parser(adress)

    
