
__author__ = 'Черепанов Дмитрий Евгеньевич'

''' Взять любую категорию товаров на сайте Леруа Мерлен. Собрать следующие данные:
- название;
- все фото;
- ссылка;
- цена.

Реализуйте очистку и преобразование данных с помощью ItemLoader. Цены должны быть в виде числового значения.

Сайт Леруа Мерлен был недоступен, поэтому сделал похожее задание для мвидео.ру'''

import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions

pics_path = r'/media/dmitriy/Disk/Downloads/geekbrains_ai_id_lesson_7_pics/'
service = Service(executable_path='/media/dmitriy/Disk/Yandex.Disk/Projects/geekbrains/ai_internet_data/lesson_7/chromedriver')
chrome_options = Options()
chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36')
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get(r'https://www.mvideo.ru/smartfony-i-svyaz-10/smartfony-205')
names, hrefs, prices = [], [], []
while True:
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//div[@class="product-cards-layout__item without-border ng-star-inserted"]')))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//a[@class="product-title__text"]')))
        elements = driver.find_elements(By.XPATH, '//div[@class="product-cards-layout__item ng-star-inserted"]')
        elements_wb = driver.find_elements(By.XPATH, '//div[@class="product-cards-layout__item without-border ng-star-inserted"]')
        elements += elements_wb
        for element in elements:
            name, href, price = None, None, None
            try:
                element_data = element.find_element(By.XPATH, './/a[@class="product-title__text"]')
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//span[@class="price__main-value"]')))
                price_data = element.find_element(By.XPATH, './/span[@class="price__main-value"]')
                name = element_data.text
                href = element_data.get_property('href')
                price = float(''.join(price_data.text[:-1].split(' ')))
                picture_data = element.find_element(By.XPATH, './/a[@class="product-picture-link"]')
                with open(os.path.join(pics_path, f'{element_data.text}.png'), 'wb') as f:
                    f.write(picture_data.screenshot_as_png)
            except Exception as e:
                pass
            if name != None:
                names.append(name)
                hrefs.append(href)
                prices.append(price)
        next_button = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//a[@class="page-link icon ng-star-inserted"]')))
        driver.execute_script("arguments[0].click();", next_button)
    except exceptions.TimeoutException:
        print('Finished')
        break
data = {'names': names, 'prices': prices, 'urls': hrefs}
mvideo_dataframe = pd.DataFrame(data)
mvideo_dataframe.to_csv(f'mvideo_smartphones.csv', index=False, encoding='utf-8', sep=',')
