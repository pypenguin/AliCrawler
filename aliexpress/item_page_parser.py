from urllib.request import urlopen
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from time import sleep

# Data mining Aliexpress (item image, title, cost, description)

opts = Options()
opts.set_headless()
assert opts.headless

driver = Firefox(options=opts)

link = "https://ru.aliexpress.com/item/33060763780.html?spm=a2g01.12375326.layer-is9wlp.1.106c67d0b1MdqF&gps-id=5895473&scm=1007.20780.114778.0&scm_id=1007.20780.114778.0&scm-url=1007.20780.114778.0&pvid=cc0fa831-1a7c-45fb-9360-43ea6ca76ee0"

driver.get(link)
pageSource = driver.page_source
bsObj = BeautifulSoup(pageSource, "html.parser")

class PageDataParser():
    def __init__(self, bsObj):
        self.bsObj = bsObj

    def get_item_img(self):
        img = self.bsObj.find(class_="magnifier-image").attrs['src']
        print(img)

    def get_item_title(self):
        title = self.bsObj.find(class_="product-title").get_text()
        print(title)

    def get_item_cost(self):
        cost = self.bsObj.find(class_="product-price-value").get_text()
        print(cost)

#----------------------------------------Main---------------------------------------------------------------------------
page_source = PageDataParser(bsObj)

page_source.get_item_img()
page_source.get_item_title()
page_source.get_item_cost()

driver.quit()
#----------------------EOF----------------------------------------------------------------------------------------------