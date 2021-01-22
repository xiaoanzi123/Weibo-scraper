#!/usr/bin/env python
# encoding: utf-8
import datetime
import os
import pymongo
from scrapy import Selector, Request
import re
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy_redis.spiders import RedisSpider

from sina.items import TweetsItem, InformationItem, TweetAndInformationItem
from sina.settings import REMOTE_MONGO_HOST, REMOTE_MONGO_PORT


class WeiboSearchSpider(RedisSpider):
    name = "chenanfan_weibo_cn_tweet_and_info_search_spider"
    redis_key = "chenanfan_weibo_cn_tweet_and_info_search_spider:start_urls"
    base_url = "https://weibo.cn"
    custom_settings = {
        'CONCURRENT_REQUESTS': 16,
        "DOWNLOAD_DELAY": 0.1,
        # "LOG_FILE": "{}.log".format(os.getpid())
    }

    def parse(self, response):
        if response.url.endswith('page=1'):
            if u'未找到' in response.text:
                self.logger.info('本页没有内容 {}'.format(response.url))
                return
            all_page = re.search(r'/>&nbsp;1/(\d+)页</div>', response.text)
            if all_page:
                all_page = all_page.group(1)
                for page_num in range(2, int(all_page) + 1):
                    page_url = response.url.replace('page=1', 'page={}'.format(page_num))
                    yield Request(page_url, self.parse, dont_filter=True)
        selector = Selector(response)
        """
        解析本页的数据
        """
        tweet_nodes = selector.xpath('body/div[@class="c" and @id]')
        for tweet_node in tweet_nodes:
            try:
                tweet_and_tweet_and_information_item = TweetAndInformationItem()
                tweet_repost_url = tweet_node.xpath('.//a[contains(text(),"转发[")]/@href').extract_first()
                user_tweet_id = re.search(r'/repost/(.*?)\?uid=(\d+)', tweet_repost_url)
                tweet_and_tweet_and_information_item['user_id'] = user_tweet_id.group(2)
                tweet_and_tweet_and_information_item['weibo_url'] = 'https://weibo.com/{}/{}'.format(
                    tweet_and_tweet_and_information_item['user_id'],
                    user_tweet_id.group(1))
                tweet_and_tweet_and_information_item['_id'] = '{}_{}'.format(
                    tweet_and_tweet_and_information_item['user_id'],
                    user_tweet_id.group(1))
                tweet_info_node = tweet_node.xpath('.//span[@class="ctt"]')[0]
                tweet_info = tweet_info_node.xpath('string(.)').extract_first()[1:]
                tweet_and_tweet_and_information_item['content'] = tweet_info.strip().replace('\u200b', '')

                create_time_node = tweet_node.xpath('.//span[@class="ct" and contains(text(),"来自")]')[0]
                create_time_info = create_time_node.xpath('string(.)').extract_first()
                tweet_and_tweet_and_information_item['created_at'] = create_time_info.split('来自')[0].strip()

                like_num = tweet_node.xpath('.//a[contains(text(),"赞")]/text()').extract_first()
                tweet_and_tweet_and_information_item['like_num'] = re.search('\d+', like_num).group()

                repost_num = tweet_node.xpath('.//a[contains(text(),"转发")]/text()').extract_first()
                tweet_and_tweet_and_information_item['repost_num'] = re.search('\d+', repost_num).group()

                comment_num = tweet_node.xpath(
                    './/a[contains(text(),"评论") and not(contains(text(),"原文"))]/text()').extract_first()
                tweet_and_tweet_and_information_item['comment_num'] = re.search('\d+', comment_num).group()

                yield Request(self.base_url + '/{}/info'.format(tweet_and_tweet_and_information_item['user_id']),
                              callback=self.parse_information, meta={'item': tweet_and_tweet_and_information_item})
            except Exception as e:
                self.logger.error(e)

        """
        解析下一页数据
        """
        next_url = selector.xpath('//a[text()="下页"]/@href').extract_first()
        self.logger.info(next_url)
        if next_url:
            yield Request(self.base_url + next_url, callback=self.parse)

    def parse_information(self, response):
        """ 抓取个人信息 """
        tweet_and_information_item = response.meta['item']
        selector = Selector(response)
        ID = re.findall('(\d+)/info', response.url)[0]
        text1 = ";".join(selector.xpath('body/div[@class="c"]//text()').extract())  # 获取标签里的所有text()
        nick_name = re.findall('昵称;?[：:]?(.*?);', text1)
        gender = re.findall('性别;?[：:]?(.*?);', text1)
        place = re.findall('地区;?[：:]?(.*?);', text1)
        briefIntroduction = re.findall('简介;[：:]?(.*?);', text1)
        birthday = re.findall('生日;?[：:]?(.*?);', text1)
        sex_orientation = re.findall('性取向;?[：:]?(.*?);', text1)
        sentiment = re.findall('感情状况;?[：:]?(.*?);', text1)
        vip_level = re.findall('会员等级;?[：:]?(.*?);', text1)
        authentication = re.findall('认证;?[：:]?(.*?);', text1)
        url = re.findall('互联网;?[：:]?(.*?);', text1)
        if nick_name and nick_name[0]:
            tweet_and_information_item["nick_name"] = nick_name[0].replace(u"\xa0", "")
        if gender and gender[0]:
            tweet_and_information_item["gender"] = gender[0].replace(u"\xa0", "")
        if place and place[0]:
            place = place[0].replace(u"\xa0", "").split(" ")
            tweet_and_information_item["province"] = place[0]
            if len(place) > 1:
                tweet_and_information_item["city"] = place[1]
        if briefIntroduction and briefIntroduction[0]:
            tweet_and_information_item["brief_introduction"] = briefIntroduction[0].replace(u"\xa0", "")
        if birthday and birthday[0]:
            tweet_and_information_item['birthday'] = birthday[0]
        if sex_orientation and sex_orientation[0]:
            if sex_orientation[0].replace(u"\xa0", "") == gender[0]:
                tweet_and_information_item["sex_orientation"] = "同性恋"
            else:
                tweet_and_information_item["sex_orientation"] = "异性恋"
        if sentiment and sentiment[0]:
            tweet_and_information_item["sentiment"] = sentiment[0].replace(u"\xa0", "")
        if vip_level and vip_level[0]:
            tweet_and_information_item["vip_level"] = vip_level[0].replace(u"\xa0", "")
        if authentication and authentication[0]:
            tweet_and_information_item["authentication"] = authentication[0].replace(u"\xa0", "")
        if url:
            tweet_and_information_item["person_url"] = url[0]
        yield Request('https://weibo.cn/u/{}'.format(ID),
                      callback=self.parse_further_information,
                      meta={'item': tweet_and_information_item}, dont_filter=True)

    def parse_further_information(self, response):
        text = response.text
        tweet_and_information_item = response.meta['item']
        tweets_num = re.findall('微博\[(\d+)\]', text)
        if tweets_num:
            tweet_and_information_item['tweets_num'] = tweets_num[0]
        follows_num = re.findall('关注\[(\d+)\]', text)
        if follows_num:
            tweet_and_information_item['follows_num'] = follows_num[0]
        fans_num = re.findall('粉丝\[(\d+)\]', text)
        if fans_num:
            tweet_and_information_item['fans_num'] = fans_num[0]
        yield tweet_and_information_item


if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl('chenanfan_weibo_cn_tweet_and_info_search_spider')
    process.start()  # the script will block here until the crawling is finished
