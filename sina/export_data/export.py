#!/usr/bin/env python
# encoding: utf-8
import os
import pandas as pd
from sina.settings import LOCAL_MONGO_PORT as MONGO_PORT, LOCAL_MONGO_HOST as MONGO_HOST


def export_operate(command, collection_name):
    os.system(command)
    csv = pd.read_csv('data.csv', encoding='utf-8')
    writer = pd.ExcelWriter('./{}.xlsx'.format(collection_name),
                            engine='xlsxwriter',
                            options={'strings_to_urls': False})
    csv.to_excel(writer, sheet_name='data')
    writer.save()
    os.remove('data.csv')


def export_tweet(collection_name):
    """
    导出微博数据，传入collection_name,对应pipelines.py中self.Tweets = db["tweet"]中的值，这里就是tweet
    """
    export_command = "mongoexport --host {} --port {} -d Sina -c {} --type=csv --fields _id,user_id,created_at,content,weibo_url,like_num,repost_num,comment_num -o data.csv".format(
        MONGO_HOST, MONGO_PORT, collection_name
    )
    export_operate(export_command, collection_name)


def export_information(collection_name):
    """
    导出用户数据，传入collection_name,对应pipelines.py中self.Information = db["information"]中的值，这里就是information
    """
    export_command = "mongoexport --host {} --port {} -d Sina -c {} --type=csv --fields _id,nick_name,gender,province,city,brief_introduction,birthday,tweets_num,follows_num,fans_num,sex_orientation,sentiment,vip_level,authentication,person_url -o data.csv".format(
        MONGO_HOST, MONGO_PORT, collection_name
    )
    export_operate(export_command, collection_name)


def export_tweet_and_information(collection_name):
    export_command = "mongoexport --host {} --port {} -d Sina -c {} --type=csv --fields _id,user_id,created_at,content,weibo_url,like_num,repost_num,comment_num,nick_name,gender,province,city,brief_introduction,birthday,tweets_num,follows_num,fans_num,sex_orientation,sentiment,vip_level,authentication,person_url -o data.csv".format(
        MONGO_HOST, MONGO_PORT, collection_name
    )
    export_operate(export_command, collection_name)


if __name__ == "__main__":
    # export_information('tweet')
    # export_information('information')
    export_tweet_and_information('ruhua_tweet_and_info')
