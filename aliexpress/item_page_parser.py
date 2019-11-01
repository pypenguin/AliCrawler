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

args_pars = ArgumentParser(description="Results in text console and csv file")
args_pars.add_argument('--text', help='text - Results in text console', action='store_true', default='False')
args_pars.add_argument('--csv', help='csv - Results in csv file', default='False')
args = args_pars.parse_args()
text = args.text
csvF = args.csv

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
        return img

    def get_product_title(self):
        title = self.bsObj.find(class_="product-title").get_text()
        return title

    def get_product_reviewer(self):
        rating = self.bsObj.find(class_="overview-rating-average").get_text()
        reviews = self.bsObj.find(class_="product-reviewer-reviews black-link").get_text()
        sold = self.bsObj.find(class_="product-reviewer-sold").get_text()
        return rating, reviews, sold

    def get_product_cost(self):
        cost = self.bsObj.find(class_="product-price-value").get_text()
        return cost

    def get_product_quantity(self):
        quantity = self.bsObj.find(class_="product-quantity-tip").get_text()
        return quantity

    def get_product_shipping(self):
        shipping_price = self.bsObj.find(class_="product-shipping-price").get_text()
        shipping_info = self.bsObj.find(class_="product-shipping-info black-link").get_text()
        shipping_delivery = self.bsObj.find(class_="product-shipping-delivery").get_text()
        return shipping_price, shipping_info, shipping_delivery

    def product_comment(self):
        print("")


#----------------------------------------Main---------------------------------------------------------------------------
sleep(30)

page_source = PageDataParser(bsObj)
productImg = page_source.get_product_img()
productTitle = page_source.get_product_title()
productReviewer = page_source.get_product_reviewer()
productCost = page_source.get_product_cost()
productQuantity = page_source.get_product_quantity()
productShipping = page_source.get_product_shipping()

data_ = [productImg, productTitle, productReviewer, productCost, productQuantity, productShipping]


#Results in text console and csv file
def dataOut(text, csvF):
    if text == True:
        print(productImg)
    if csvF == True:
        outCsvFile(data_)
dataOut(text, csvF)

#Write results in csv file
def outCsvFile(data_):
    try:
        csvFile = open('aliexpress.txt', 'wt')
        writer = csv.writer(csvFile, delimiter='|')
        writer.writerow(data_)
    finally:
        csvFile.close()
outCsvFile(data_)


driver.quit()

print("--- %s seconds ---" % (time() - start_time))
#----------------------EOF----------------------------------------------------------------------------------------------