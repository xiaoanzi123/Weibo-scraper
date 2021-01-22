# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field, Item


class TweetsItem(Item):
    """ 微博信息 """
    _id = Field()
    user_id = Field()
    created_at = Field()
    content = Field()
    weibo_url = Field()
    like_num = Field()
    repost_num = Field()
    comment_num = Field()


class InformationItem(Item):
    """ 个人信息 """
    _id = Field()  # 用户ID
    nick_name = Field()  # 昵称
    gender = Field()  # 性别
    province = Field()  # 所在省
    city = Field()  # 所在城市
    brief_introduction = Field()  # 简介
    birthday = Field()  # 生日
    tweets_num = Field()  # 微博数
    follows_num = Field()  # 关注数
    fans_num = Field()  # 粉丝数
    sex_orientation = Field()  # 性取向
    sentiment = Field()  # 感情状况
    vip_level = Field()  # 会员等级
    authentication = Field()  # 认证
    person_url = Field()  # 首页链接


class TweetAndInformationItem(Item):
    _id = Field()  # 唯一ID
    user_id = Field()  # 用户ID
    created_at = Field()  # 微博发布时间
    content = Field()  # 微博内容
    weibo_url = Field()  # 微博URL
    like_num = Field()  # 微博点赞数
    repost_num = Field()  # 微博转发数
    comment_num = Field()  # 微博评论数
    nick_name = Field()  # 用户昵称
    gender = Field()  # 用户性别
    province = Field()  # 用户所在省
    city = Field()  # 用户所在城市
    brief_introduction = Field()  # 用户简介
    birthday = Field()  # 用户生日
    tweets_num = Field()  # 用户微博数
    follows_num = Field()  # 用户关注数
    fans_num = Field()  # 用户粉丝数
    sex_orientation = Field()  # 用户性取向
    sentiment = Field()  # 用户感情状况
    vip_level = Field()  # 用户会员等级
    authentication = Field()  # 用户认证情况
    person_url = Field()  # 用户首页链接


class CommentItem(Item):
    """
    微博评论信息
    """
    _id = Field()
    comment_user_id = Field()
    content = Field()
    weibo_url = Field()
