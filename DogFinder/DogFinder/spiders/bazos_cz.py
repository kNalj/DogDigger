# -*- coding: utf-8 -*-
import scrapy
from ..items import DogfinderItem


class BazosSkSpider(scrapy.Spider):
    name = 'bazos_cz'
    allowed_domains = ['zvirata.bazos.cz']
    start_urls = ['https://zvirata.bazos.cz/pes/']

    def parse(self, response):

        add_selector = ".vypis"
        next_page_selector = ".strankovani ::attr(href)"
        next_page_title_selector = ".strankovani ::text"

        for add in response.css(add_selector):
            title_selector = ".nadpis ::text"
            date_selector = ".velikost10 ::text"
            description_selector = ".popis ::text"
            link_selector = ".nadpis ::attr(href)"

            dog_add = DogfinderItem()
            dog_add["id"] = add.css(link_selector).extract_first().split("/")[-2]
            dog_add["title"] = add.css(title_selector).extract_first()
            dog_add["date"] = add.css(date_selector).extract_first()[4:-1]
            dog_add["description"] = add.css(description_selector).extract_first()
            dog_add["link"] = "https://zvirata.bazos.cz" + add.css(link_selector).extract_first()

            yield dog_add

        for page in [response.css(next_page_selector).getall()[-1]]:
            page_size = page.strip("/").split("/")[-1]
            if int(page_size) <= 200:
                link_text = response.css(next_page_title_selector).getall()[-1]
                if link_text == "Další":
                    print("Attempting to go to location: {}".format("https://zvirata.bazos.cz" + page))
                    yield response.follow("https://zvirata.bazos.cz" + page, self.parse)
