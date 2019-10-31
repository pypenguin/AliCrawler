#!/usr/bin/env python3
import os
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from time import sleep, time
from sys import exit
import yaml
from argparse import ArgumentParser
import csv

# Data mining Aliexpress (product image, title, cost, description, comment)

start_time = time()

args_pars = ArgumentParser(description="Output data parser text in console and to send email")
args_pars.add_argument('--text', help='text - Output text in console', action='store_true', default='False')
args_pars.add_argument('--csv', help='csv - Output text in file csv', default='False')
args_pars.add_argument('--email', help='email - Output to send email', action='store_true', default='False')
args = args_pars.parse_args()
text = args.text
csvF = args.csv
email = args.email

# load file configuration
try:
    config = yaml.load(open('config.conf'))
except IOError:
    print("!!! Error: can't read file configuration config.conf")
    exit()

# open tor browser
startTor = (os.popen('../tor-browser_ru/Browser/start-tor-browser'))
print('run tor browser wait 5 sec')
sleep(5)

service_args = ['--proxy=localhost:9150', '--proxy-type=socks5', ]

opts = Options()
opts.set_headless()
assert opts.headless

profile = FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.socks", '127.0.0.1')
profile.set_preference("network.proxy.socks_port", 9150)
profile.set_preference("network.proxy.socks_remote_dns", False)
profile.update_preferences()

driver = Firefox(options=opts, firefox_profile=profile)

link = config['path_link']

def badLink(link):
    try:
        driver.get(link)
    except WebDriverException:
        print("Reached error page")
        exit()

badLink(link)

pageSource = driver.page_source

bsObj = BeautifulSoup(pageSource, "html.parser")


class PageDataParser():
    def __init__(self, bsObj):
        self.bsObj = bsObj

    def get_product_img(self):
        img = self.bsObj.find(class_="magnifier-image").attrs['src']
        print(img)

    def get_product_title(self):
        title = self.bsObj.find(class_="product-title").get_text()
        print(title)

    def get_product_reviewer(self):
        rating = self.bsObj.find(class_="overview-rating-average").get_text()
        reviews = self.bsObj.find(class_="product-reviewer-reviews black-link").get_text()
        sold = self.bsObj.find(class_="product-reviewer-sold").get_text()
        print(rating)
        print(reviews)
        print(sold)

    def get_product_cost(self):
        cost = self.bsObj.find(class_="product-price-value").get_text()
        print(cost)

    def get_product_quantity(self):
        quantity = self.bsObj.find(class_="product-quantity-tip").get_text()
        print(quantity)

    def get_product_shipping(self):
        shipping_price = self.bsObj.find(class_="product-shipping-price").get_text()
        shipping_info = self.bsObj.find(class_="product-shipping-info black-link").get_text()
        shipping_delivery = self.bsObj.find(class_="product-shipping-delivery").get_text()
        print(shipping_price)
        print(shipping_info)
        print(shipping_delivery)

    def product_comment(self):
        print("")


#----------------------------------------Main---------------------------------------------------------------------------
sleep(15)

page_source = PageDataParser(bsObj)
_product_img = page_source.get_product_img()
_product_title = page_source.get_product_title()
_product_reviewer = page_source.get_product_reviewer()
_product_cost = page_source.get_product_cost()
_product_quantity = page_source.get_product_quantity()
_product_shipping = page_source.get_product_shipping()

csvFile = open('aliexpress.txt', 'wt')

def outputCsv(csvFile):
    try:
        writer = csv.writer(csvFile)
        writer.writerow(('img', 'title', 'reviewer', 'cost', 'quantyty, shipping'))
        for product_img_, product_title_, product_reviewer_, product_cost_, product_quantity_, product_shipping_ in _product_img, _product_title, _product_reviewer, _product_cost, _product_quantity, _product_shipping:
            writer.writerow(
                (product_img_, product_title_, product_reviewer_, product_cost_, product_quantity_, product_shipping_))
    finally:
        csvFile.close()

outputCsv(csvFile)

# Data Output text in console and to send email
def dataOutput(text, email):
    if text == True:
        print(_product_img,
        _product_title,
        _product_reviewer,
        _product_cost,
        _product_quantity,
        _product_shipping)
    if email == True:
        print("send to email")

dataOutput(text, email)

driver.quit()

print("--- %s seconds ---" % (time() - start_time))
#----------------------EOF----------------------------------------------------------------------------------------------