# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from pymongo.errors import DuplicateKeyError

from sina.items import TweetsItem, InformationItem, TweetAndInformationItem
from sina.settings import LOCAL_MONGO_PORT, LOCAL_MONGO_HOST, REMOTE_MONGO_PORT, REMOTE_MONGO_HOST


class MongoDBPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(LOCAL_MONGO_HOST, LOCAL_MONGO_PORT)
        db = client["Sina"]
        # 这里对应的是collection的名字
        self.Tweets = db["tweet"]
        self.Information = db["information"]
        self.tweet_and_info = db["sujia_tweet_and_info"]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, TweetsItem):
            self.insert_item(self.Tweets, item)
        if isinstance(item, InformationItem):
            self.insert_item(self.Information, item)
        if isinstance(item, TweetAndInformationItem):
            self.insert_item(self.tweet_and_info, item)
        return item

    def insert_item(self, collection, item):
        try:
            collection.insert(dict(item))
        except DuplicateKeyError:
            """
            说明有重复数据
            """
            pass
