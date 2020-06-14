# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class DogfinderPipeline(object):

    def __init__(self):
        self.keywords = ["bernsky", "bernský", "salašnicky", "border", "collie", "labrador", "bernese",
                         "bordernese", "kolia", "borderska", "australsky", "austrálsky", "bernski", "planšar",
                         "sennenhund", "berner", "appenzeller"]

        self.avoid_words = ["koupim", "krytie", "kupim"]

    def process_item(self, item, spider):
        if self.scan_for_keywords(item):
            # send email
            return item
        else:
            return None
        return item

    def scan_for_keywords(self, item):
        for keyword in self.keywords:
            if (keyword in item["description"]) or (keyword in item["title"]):
                for word in self.avoid_words:
                    if (word in item["description"]) or (word in item["title"]):
                        return False
                return True
        return False