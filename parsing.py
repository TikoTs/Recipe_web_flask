import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
from app import Recipes, db, Meals


numb = 0
length = 0
item_name_str = 'smth'
l_ingr = []
l_steps = []
l_item_src = []
h = {'Accept-language': '*', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'}
index = 1
#
# #parsing of cocktails recipes
while index < 5:
    url = 'https://www.bbcgoodfood.com/recipes/collection/easy-cocktail-recipes?page=' + str(index)
    r = requests.get(url, headers=h)
    soup = BeautifulSoup(r.text, 'html.parser')
    soup_sub = soup.find('div', class_="post__content")
    all_items = soup_sub.find_all('li', class_="dynamic-list__list-item list-item")
    index += 1
    sleep(randint(1, 3))
    for item in all_items:
        item_name = item.h2.text
        if item_name_str is not item_name:
            item_name_str = item_name
            l_ingr.clear()
            l_steps.clear()
            numb = 0
        for one in item_name:
            if one == ' ':
                item_name = item_name.replace(one, '-')

        url_new = "https://www.bbcgoodfood.com/recipes/" + item_name
        r_new = requests.get(url_new, headers=h)
        soup_new = BeautifulSoup(r_new.text, 'html.parser')
        soup_sub_ingr = soup_new.find('section', class_='recipe__ingredients col-12 mt-md col-lg-6')
        soup_sub_steps = soup_new.find('section', class_='recipe__method-steps mb-lg col-12 col-lg-6')
        soup_sub_img = soup_new.find('div', class_='post-header__image-container')
        try:
            all_ingredients = soup_sub_ingr.find_all('li', class_='pb-xxs pt-xxs list-item list-item--separator')

            for one in all_ingredients:
                ingredient = one.text
                l_ingr.append(ingredient)
            length = len(l_ingr)
            all_steps = soup_sub_steps.find_all('li', class_='pb-xs pt-xs list-item')
            for each in all_steps:
                step = each.text
                l_steps.append(step)
            pict = soup_sub_img.find_all('img', class_="image__img")
            for one in pict:
                source = one['src']
            recipe_obj = Recipes(name=item_name_str, ingredients=str(l_ingr),
                                  recipe_steps=str(l_steps), ingredients_numb=length, item_src=source)
            db.session.add(recipe_obj)
            db.session.commit()
        except AttributeError:
            pass


# # parsing of meals recipes
while index < 3:
    url = 'https://www.bbcgoodfood.com/recipes/collection/cheap-and-healthy-recipes?page=' + str(index)
    r = requests.get(url, headers=h)
    soup = BeautifulSoup(r.text, 'html.parser')
    soup_sub = soup.find('div', class_="post__content")
    all_items = soup_sub.find_all('li', class_="dynamic-list__list-item list-item")
    index += 1
    sleep(randint(1, 3))
    for item in all_items:
        item_name = item.h2.text
        if item_name_str is not item_name:
            item_name_str = item_name
            l_ingr.clear()
            l_steps.clear()
            numb = 0
        for one in item_name:
            if one == ' ':
                item_name = item_name.replace(one, '-')

        url_new = "https://www.bbcgoodfood.com/recipes/" + item_name
        r_new = requests.get(url_new, headers=h)
        soup_new = BeautifulSoup(r_new.text, 'html.parser')
        soup_sub_ingr = soup_new.find('section', class_='recipe__ingredients col-12 mt-md col-lg-6')
        soup_sub_steps = soup_new.find('section', class_='recipe__method-steps mb-lg col-12 col-lg-6')
        soup_sub_img = soup_new.find('div', class_='post-header__image-container')
        try:
            all_ingredients = soup_sub_ingr.find_all('li', class_='pb-xxs pt-xxs list-item list-item--separator')

            for one in all_ingredients:
                ingredient = one.text
                l_ingr.append(ingredient)
            length = len(l_ingr)   #იმიტომ, რომ ბოლოში წერია გარნირი
            all_steps = soup_sub_steps.find_all('li', class_='pb-xs pt-xs list-item')
            for each in all_steps:
                step = each.text
                l_steps.append(step)
            pict = soup_sub_img.find_all('img', class_="image__img")
            for one in pict:
                source = one['src']
            meals_obj = Meals(name=item_name_str, ingredients=str(l_ingr),
                                  recipe_steps=str(l_steps), item_src=source)
            db.session.add(meals_obj)
            db.session.commit()
        except AttributeError:
            pass
