
from selenium import webdriver
import sys
import time
import pandas as pd
import os

path = os.curdir
filepath = os.path.join(path, "movies_Ryan_Gosling.csv")




driver  = webdriver.Chrome('./src/chromedriver')

def has_item(xpath, driver = driver):
    try:
        driver.find_element('xpath', xpath)
        return True
    except:
        return False


time.sleep(5)
driver.implicitly_wait(40)
driver.get('https://pt.wikipedia.org/wiki/Ryan_Gosling')

xp_filmes = '/html/body/div[1]/div/div[4]/main/div[2]/div[3]/div[1]/table[2]'

i = 0
while not has_item(xp_filmes):
    i+=1
    if i > 50:
        break
    pass


table = driver.find_element('xpath', xp_filmes)
df = pd.read_html('<table>' + table.get_attribute('innerHTML') + '</table>')[0]
driver.close()
df.to_csv(filepath, sep=';', index=False)


