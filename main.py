import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def main():
    print(os.getcwd())
    os.chdir("./DogFinder")
    print(os.getcwd())

    process = CrawlerProcess(get_project_settings())
    process.crawl("bazos_sk")
    process.crawl("bazos_cz")
    process.crawl("bolha_com")
    process.crawl("landwirt_com")
    process.start()


if __name__ == "__main__":
    main()
