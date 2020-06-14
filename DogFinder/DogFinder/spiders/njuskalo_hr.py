# -*- coding: utf-8 -*-
import scrapy
from ..items import DogfinderItem


class NjuskaloHrSpider(scrapy.Spider):
    name = 'njuskalo_hr'
    allowed_domains = ['www.njuskalo.hr']
    start_urls = ['https://www.njuskalo.hr/kucni-ljubimci/']

    def parse(self, response):

        add_selector = ".entity-body cf"
        next_page_selector = ".div.PaginationContainer:nth-child(10) > nav:nth-child(1) > ul:nth-child(1) > li:nth-child(8)"
        next_page_title_selector = ".strankovani ::text"

        for add in response.css(add_selector):
            title_selector = ".entity-title ::text"
            date_selector = ".entity-pub-date ::text"
            description_selector = ".entity-description ::text"
            link_selector = ".link ::attr(href)"

            dog_add = DogfinderItem()
            dog_add["id"] = add.css(link_selector).extract_first().split("/")[-2]
            dog_add["title"] = add.css(title_selector).extract_first()
            dog_add["date"] = add.css(date_selector).extract_first()[4:-1]
            dog_add["description"] = add.css(description_selector).extract_first()
            dog_add["link"] = "https://www.njuskalo.hr" + add.css(link_selector).extract_first()

            yield dog_add

        # for page in [response.css(next_page_selector)]:
        #     page_size = page.strip("/").split("/")[-1]
        #     if int(page_size) <= 200:
        #         link_text = response.css(next_page_title_selector).getall()[-1]
        #         if link_text == "Ďalšia":
        #             print("Attempting to go to location: {}".format("https://zvierata.bazos.sk" + page))
        #             yield response.follow("https://www.njuskalo.hr" + page, self.parse)
