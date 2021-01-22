# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import pymongo
import random

from scrapy import Request

from sina.settings import REMOTE_MONGO_HOST, REMOTE_MONGO_PORT


class CookieMiddleware(object):
    """
    每次请求都随机从账号池中选择一个账号去访问
    """

    def __init__(self):
        mongo_client = pymongo.MongoClient(REMOTE_MONGO_HOST, REMOTE_MONGO_PORT)
        self.collection = mongo_client["Sina"]["weibo_cn_account"]

    def process_request(self, request, spider):
        self.all_count = self.collection.count()
        random_index = random.randint(0, self.all_count - 1)
        random_account = self.collection.find()[random_index]
        request.headers.setdefault('Cookie', random_account['cookie'])
        request.meta['account'] = random_account


class RedirectMiddleware(object):
    def __init__(self):
        mongo_client = pymongo.MongoClient(REMOTE_MONGO_HOST, REMOTE_MONGO_PORT)
        self.account_collection = mongo_client["Sina"]["weibo_cn_account"]
        self.error_account_collection = mongo_client["Sina"]["weibo_cn_error_account"]

    def process_response(self, request, response, spider):
        http_code = response.status
        if http_code == 302:
            try:
                self.account_collection.delete_one({"_id": request.meta['account']['_id']})
                self.error_account_collection.insert(request.meta['account'])
            except Exception as e:
                print(e)
            return Request(url=request.meta['url'], meta={'url': request.meta['url']}, dont_filter=True)
        else:
            return response