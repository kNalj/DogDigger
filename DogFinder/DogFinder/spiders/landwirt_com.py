# -*- coding: utf-8 -*-
import scrapy
from ..items import DogfinderItem


class LandwirtComSpider(scrapy.Spider):
    name = 'landwirt_com'
    allowed_domains = ['www.landwirt.com']
    start_urls = ['https://www.landwirt.com/Kleinanzeigen/angebote-Hunde,74.html']

    def parse(self, response):

        add_selector = ".gmmtreffer"

        for add in response.css(add_selector):
            title_selector = ".kleinzeigenlisteheader ::text"
            date_selector = ".gmmlinkbox ::text"
            description_selector = ".classified-preview ::text"
            link_selector = ".kleinzeigenlisteheader ::attr(href)"

            dog_add = DogfinderItem()
            dog_add["id"] = add.css(link_selector).extract_first()
            dog_add["title"] = add.css(title_selector).extract_first()
            dog_add["date"] = add.css(date_selector).extract_first()
            dog_add["description"] = add.css(description_selector).extract_first()
            dog_add["link"] = "https://www.landwirt.com" + add.css(link_selector).extract_first()

            yield dog_add
