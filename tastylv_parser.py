#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as Ureq
import re
import itertools
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

# Get tasty.lv recipe categories urls. Run this function once.
cat_url = 'https://www.delfi.lv/tasty/receptes/'
def tasty_categories_urls(cat_url):
    uClient = Ureq(cat_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    url_list_long = []
    urls = page_soup.findAll('div', {'col-sm-12 col-lg-6'})
    for url in urls:
        url_list_long.append(url.find('a')['href'])
    for url_all in url_list_long:
        with open(os.path.join(__location__, "category_urls.txt"), "a") as tasty_cat:
            tasty_cat.write(url_all + '\n')

# Get recipe urls from all pages in categories
def recipe_urls():
    with open(os.path.join(__location__, "category_urls.txt")) as categories:
        lines = categories.readlines()
        urls = []
        for line in lines:
            urls.append("https://www.delfi.lv" + line.rstrip('\n'))
        for number, url in enumerate(urls):  
            print(number, url)    # Print numbered recipe categories url list
        pages_url = []
        url_list_long = []
        for x in range(1, 10):       # Can take longer time to process if range is large
            pages_url.append(urls[60] + "?page=" + str(x))    # Put recipe category index in urls[]
        for url in pages_url:
            try:
                uClient = Ureq(url) 
                page_html = uClient.read()
                uClient.close()
                page_soup = soup(page_html, "html.parser")
                links = page_soup.findAll(
                    "span", {"class": "text-size-22 text-size-md-19 d-block"})
                for div in links:
                    url_list_long.append(div.find('a')['href'])
            except:
                pass
        with open(os.path.join(__location__, "tasty_recipes_url.txt"), "w") as f:
            for url in url_list_long:
                f.write(url + '\n')

adress = ""   # Put here recipe url from tasty_recipes_url.txt

# Parsing recipe and cleaning results
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>', )
    cleantext = re.sub(cleanr, '', raw_html)
    return(cleantext)

def info_parsing(adress):
    uClient = Ureq(adress)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")

    # Recipe title

    title = page_soup.find("div", {"class": "text-size-12 font-weight-bold"})

    # Recipe description

    description = page_soup.find("p", {"class": "font-weight-bold"})

    # Cooking instructions

    cooking_raw = page_soup.find('p').find_next_siblings('p')
    cooking = cleanhtml(str(cooking_raw))

    # Create dictionary from ingredients and yields

    recipe_ingredients = []
    amount = []
    ingredients_html = page_soup.findAll(itemprop="recipeIngredient")
    for ingredients in ingredients_html:
        recipe_ingredients.append(ingredients.getText().split('\n')[0].strip())
    amount_html = page_soup.find_all(
        'div', {'col-4 my-auto font-italic ing-amount text-center'})
    for a in amount_html:
        amount.append(a.getText().split('\n')[0].strip())
    ingredients_amount = dict(zip(recipe_ingredients, amount))

    # Recipe title, cooking dificulty, cooking time, serving discription, portions.

    for ie in ingredients_amount.items():
        print(title.text)

        try:
            print("Sarežģītība:", page_soup.find(
                "span", class_="recipe-difficulty font-weight-bold").text)
        except:
            pass
        try:
            print("Pagatavošanas laiks:", page_soup.find(
                itemprop="cookTime totalTime").text)
        except:
            pass
        try:
            print("Porcijas:", page_soup.find(itemprop="recipeYield").text)
        except:
            pass
        try:
            print("Pasniegšana:", page_soup.find(
                "span", class_="serving-method").text)
        finally:
            print("Sastāvdaļas:")
            for (key, values) in ingredients_amount.items():
                print(key, "-",  values)
        #    print(description.text)
            print("Pagatavošana:")
            print(cooking)
            break
    else:
        print('Recepte nav atrasta. Mēģiniet vēlreiz...')


if if __name__ == "__main__":
    tasty_categories_urls(cat_url)  
    recipe_urls()
    info_parsing(adress)