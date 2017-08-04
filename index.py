from bs4 import BeautifulSoup
from selenium import webdriver
import re
import logging
import json
import time

driver = webdriver.Firefox()
GRAMS_TO_OUNCES = .03527396195

BASE_URL = "http://www.coffeereview.com/review/page/"
def get_info_from_review(review_link):
    print(review_link)
    driver.get(review_link)
    html = driver.page_source
    soup = BeautifulSoup(html, "html5lib")
    try:
        col1 = soup.find('div', {'class': 'review-col1'})
        review_rating = col1.find('div', {'class': 'review-rating'}).text
        review_title = col1.find('h2', {'class': 'review-title'}).text
        data_list = col1.find_all('p')
        coffee_entry = {}
        keys = ['location', 'origin', 'roast', 'cost']
        for i,d in enumerate(data_list):
            coffee_entry[keys[i]] = d.find('strong').text
        s_cost = coffee_entry['cost']
        total_cost = float(re.search('^\$[\d\.]+', s_cost).group(0)[1:])
        units = float(re.search('[/][\d]+', s_cost).group(0)[1:])
        unit = re.search('\w+$', s_cost).group(0)
        if unit == 'grams':
            ounces = units * GRAMS_TO_OUNCES
        else:
            ounces = units
        cost_per_ounce = total_cost/ounces

        coffee_entry["cost_per_ounce"] = cost_per_ounce
        coffee_entry["rating"] = review_rating
        coffee_entry["title"] = review_title
        return coffee_entry

    except Exception as e:
        logging.exception('message')

def get_info_from_list_page(n, data):
    driver.get(BASE_URL+ str(n) + '/')
    html = driver.page_source
    soup = BeautifulSoup(html, "html5lib")
    reviews = soup.findAll('div', class_= 'review-entry clearfix')
    for review in reviews:
        time.sleep(1)
        review_link = review.find('div', {'class': 'review-col1'}).find('h2').find('a').get('href')
        coffee_json = get_info_from_review(review_link)
        if coffee_json is not None:
            data.append(coffee_json)


def scrape():
    MAX_PAGES = 230
    n = 1
    data = []
    while n < MAX_PAGES:
        get_info_from_list_page(n, data)
        n += 1

    with open('data.txt', 'w') as f:
        json.dump(data, f, ensure_ascii=False)

scrape()
