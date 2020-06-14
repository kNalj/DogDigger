# -*- coding: utf-8 -*-
import scrapy
from ..items import DogfinderItem


class BolhaComSpider(scrapy.Spider):
    name = 'bolha_com'
    allowed_domains = ['www.bolha.com']
    start_urls = ['https://www.bolha.com/psi/']

    def parse(self, response):

        add_selector = "li.EntityList-item--Regular"
        next_page_selector = "div.PaginationContainer > nav > ul > li > button ::attr(data-page)"
        next_page_title_selector = "div.PaginationContainer > nav > ul > li > button ::text"

        for add in response.css(add_selector):

            title_selector = "li.EntityList-item--Regular > article > h3 > a ::text"
            date_selector = "li.EntityList-item--Regular > article > div > time ::text"
            description_selector = "li.EntityList-item--Regular > article > div > div ::text"
            link_selector = "li.EntityList-item--Regular > article > h3 > a ::attr(href)"
            id_selector = "li.EntityList-item--Regular > article > h3 > a ::attr(name)"

            dog_add = DogfinderItem()
            dog_add["id"] = add.css(id_selector).extract_first()
            dog_add["title"] = add.css(title_selector).extract_first()
            dog_add["date"] = add.css(date_selector).extract_first()
            dog_add["description"] = add.css(description_selector).extract_first()
            dog_add["link"] = "https://www.bolha.com" + add.css(link_selector).extract_first()

            yield dog_add

        for page in [response.css(next_page_selector).extract()[-1]]:
            print("Attempting to go to location: {}".format("https://www.bolha.com/psi?page=" + page))
            yield response.follow("https://www.bolha.com/psi?page=" + page, self.parse)
