# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class ParseVacanciesPipeline:
    def __init__(self):
        MONGO_URL = "mongodb://localhost:27017/"
        MONGO_DATABASE = 'vacancy_db'

        client = MongoClient(MONGO_URL)
        self.mongo_base = client[MONGO_DATABASE]


    def process_item(self, item, spider):
        vacancy_name = ''.join(item['name'])

        salary_min = item['salary'][0]
        salary_max = item['salary'][1]
        salary_currency = item['salary'][2]
        vacancy_link = item['vacancy_link']
        site_scraping = item['site_scraping']

        vacancy_json = {
            'vacancy_name': vacancy_name, \
            'salary_min': salary_min, \
            'salary_max': salary_max, \
            'salary_currency': salary_currency, \
            'vacancy_link': vacancy_link, \
            'site_scraping': site_scraping
        }

        collection = self.mongo_base[spider.name]
        collection.insert_one(vacancy_json)
        return vacancy_json
    

    def _get_name_currency(self, currency_name):
        currency_dict  = {
            'EUR': {'€'}, \
            'KZT': {'₸'}, \
            'RUB': {'₽', 'руб.'}, \
            'UAH': {'₴', 'грн.'}, \
            'USD': {'$'}
        }
        name = None
        for item_name, items_list in currency_dict.items():
            if currency_name in items_list:
                name = item_name
        return name
