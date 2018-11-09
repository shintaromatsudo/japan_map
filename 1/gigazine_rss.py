# -*- coding: utf-8 -*-
import sys
import json
import nltk
import numpy
import feedparser
import urllib.request
from bs4 import BeautifulSoup
import re
import pymongo

#reload(sys)
#sys.setdefaultencoding('utf-8')

DATABASE_NAME = 'gigazine'
COLLECTION_NAME = '1'

class Gigazine_RSS:
    def __init__(self):
        pass


    def save(self):
        rss = self.__get_rss()
        self.__save_rss(rss)

        return rss


    def __get_rss(self):
        rss_url = 'http://feed.rssad.jp/rss/gigazine/rss_2.0'
        articles = feedparser.parse(rss_url)

        rss = []
        for e in articles.entries:
            dic = {
                'id': e.id,
                'updated': e.updated,
                'title': e.title,
                'link': e.link,
                'summary': self.__getTextOnly(BeautifulSoup(e.summary))
            }
            rss.append(dic)

        return rss


    # Extract the text from an HTML page (no tags)
    def __getTextOnly(self, soup):
        v = soup.string  # Split by tags and check whether nested tags
        if v == None:  # If tags are nested
            c = soup.contents  # Eliminate outmost tags
            resulttext = ''
            for t in c:
                subtext = self.__getTextOnly(t)
                # If the subtext is null(u''), don't append it
                if len(subtext) > 0:
                    resulttext += subtext + '\n'
            return resulttext
        else:
            return v.strip()  # Eliminate '\n'


    def __save_rss(self, data):
        client = pymongo.MongoClient('localhost', 27017)
        db = client[DATABASE_NAME]
        co = db[COLLECTION_NAME]
        co.drop()

        co.insert(data)


    def read(self):
        client = pymongo.MongoClient('localhost', 27017)
        db = client[DATABASE_NAME]
        co = db[COLLECTION_NAME]

        data = [d for d in co.find()]

        rss = []
        for c in co.find():
            c.pop('_id', None)
            rss.append(c)

        return rss


if __name__ == '__main__':
    Gigazine_RSS().save()
    #Gigazine_RSS().read()
