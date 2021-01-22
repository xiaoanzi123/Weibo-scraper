#!/usr/bin/env python
# encoding: utf-8
import redis
import datetime

from sina.settings import REDIS_PORT, REDIS_HOST

if __name__ == "__main__":
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    for key in r.scan_iter("chenanfan_weibo_cn_tweet_and_info_search_spider*"):
        r.delete(key)
    url_format = "https://weibo.cn/search/mblog?hideSearchFrame=&keyword={}&advancedfilter=1&starttime={}&endtime={}&sort=time&page=1"
    # 搜索的关键词，可以修改
    keyword = "转基因大豆 致癌"
    # 搜索的起始日期，可修改 微博的创建日期是2009-08-16 也就是说不要采用这个日期更前面的日期了
    date_start = datetime.datetime.strptime("2013-06-21", '%Y-%m-%d')
    # 搜索的结束日期，可修改
    date_end = datetime.datetime.strptime("2018-12-14", '%Y-%m-%d')
    time_spread = datetime.timedelta(days=1)
    while date_start < date_end:
        next_time = date_start + time_spread
        url = url_format.format(keyword, date_start.strftime("%Y%m%d"), next_time.strftime("%Y%m%d"))
        r.lpush('chenanfan_weibo_cn_tweet_and_info_search_spider:start_urls', url)
        date_start = next_time
        print('添加{}成功'.format(url))
