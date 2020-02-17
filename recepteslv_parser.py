#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import bs4 as bs
import urllib.request


#Get recipe urls form category pagination. 
category_url = "https://receptes.tvnet.lv/recepsu-kolekcijas/vegetaras?page=" 
def tvnet_recipe_urls(url):
    for x in range(1,2):  # Takes time to process, change range to get all pages
        source = urllib.request.urlopen(category_url + str(x)).read()
        page_soup = bs.BeautifulSoup(source, "lxml")
        try:
            for url in page_soup.find_all('a', class_='recipe-teaser__link'):
                print(url.get('href')) 
        except:
            pass

# Get recipe urls from ingredients or category search results
search_url = 'https://receptes.tvnet.lv/search?query=pank%C5%ABkas&page='
def tvnet_search_recipe(search_url):
    for x in range(1, 2):   # Takes time to process, change range to get all pages
        try:
            source = urllib.request.urlopen(search_url + str(x)).read()
            page_soup = bs.BeautifulSoup(source, "lxml")
            for url in page_soup.find_all('a', class_='recipe-teaser__link'):
                print(url.get('href'))
        except:
            pass

recipe_url = ""  #  Put here recipe url

# Parsing recipe description
def tvnet_recipe_parser(recipe_url):
        
    source = urllib.request.urlopen(recipe_url).read()
    page_soup=bs.BeautifulSoup(source, "lxml")

    # Recipe title
    title = page_soup.find('h1', {'class': 'recipe__title'})
    print(title.text.strip())

    # Recipe ingredients
    for url in page_soup.find_all('li', class_='recipe-ingredients__item'):
        print(url.getText().strip())

    #Cooking time
    cooktime = page_soup.find('span', {'class': 'recipe-steps__cook-time'})
    print("Pagatavošanas laiks:" + cooktime.text)

    # Recipe story
    story = page_soup.find('div', {'class': 'recipe__story.node-text.recipe-story'})
    if story:
        try:
            print(story.getText.strip())
        except:
            pass

    # Recipe description
    for description in page_soup.find_all('li', class_='left-col'):
        print(description.getText().strip())



if __name__ == "__main__":
    tvnet_recipe_urls(category_url)
    tvnet_recipe_parser(recipe_url)
    



                                









 

