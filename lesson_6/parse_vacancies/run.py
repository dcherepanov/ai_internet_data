from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from parse_vacancies import settings
from parse_vacancies.spiders.hh_ru import HhRuSpider


if __name__ == '__main__':
    vacancy = 'Python'
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(HhRuSpider, vacancy=vacancy)
    process.start()