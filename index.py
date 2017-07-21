from bs4 import BeautifulSoup
from selenium import webdriver
from pymongo import MongoClient
import re

driver = webdriver.Chrome()

BASE_URL = "http://www.coffeereview.com/review/"
def get_info_from_review(review_link):
    print(review_link)
    driver.get(review_link)
    html = driver.page_source
    soup = BeautifulSoup(html, "html5lib")

    col1 = soup.find('div', {'class': 'review-col1'})
    review_rating = col1.find('div', {'class': 'review-rating'}).text
    review_title = col1.find('div', {'class': 'review-title'}).text
    location = col1.find('p', text=re.compile(r'Location'))
    print('Review Rating: ', review_rating)
    print('Review Title: ', review_title)
    print('Loaction: ', location)

def get_info_from_list_page():
    driver.get(BASE_URL)
    html = driver.page_source
    soup = BeautifulSoup(html, "html5lib")
    reviews = soup.findAll('div', {'class': ['review', 'type-review', 'status-publish', 'hentry pmpro-has-access']})
    for review in reviews:
        review_link = review.find('div', {'class': 'review-col1'}).find('h2').find('a').get('href')
        get_info_from_review(review_link)

get_info_from_list_page()
