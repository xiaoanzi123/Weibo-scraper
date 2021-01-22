# -*- coding: utf-8 -*-

BOT_NAME = 'sina'

SPIDER_MODULES = ['sina.spiders']
NEWSPIDER_MODULE = 'sina.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) Gecko/20100101 Firefox/61.0',
}

DOWNLOADER_MIDDLEWARES = {
    'weibo.middlewares.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': None,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    'sina.middlewares.CookieMiddleware': 300,
    'sina.middlewares.RedirectMiddleware': 200,

}

ITEM_PIPELINES = {
    'sina.pipelines.MongoDBPipeline': 300,
}

# Redis配置
# 增加关于Scrapy-Redis的配置
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
SCHEDULER_PERSIST = True

# 指定redis的地址和端口(可选，程序将使用默认的地址localhost:6379)
REDIS_HOST = '118.144.88.212'
REDIS_PORT = 16379

# MongoDb 配置
REMOTE_MONGO_HOST = '118.144.88.212'
REMOTE_MONGO_PORT = 19826

LOCAL_MONGO_HOST = '127.0.0.1'
LOCAL_MONGO_PORT = 27017

# LOG_LEVEL = 'INFO'
