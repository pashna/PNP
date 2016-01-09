__author__ = 'popka'

import unittest
from Engine.PagesLoaders.RSSLoader import RSSLoader
import random
import dateutil

class RSS_Tests(unittest.TestCase):
    OK = ["https://nplus1.ru/rss", "http://tass.ru/rss/export/index.xml?feed=v2"]

    def test_loading(self):
        rss_loader = RSSLoader()

        rss_loader._pages = ["http://kp.ru/rss/allsections.xml"]
        news_array = rss_loader.get_news_array()

        n = 4

        print news_array[n]["type"]
        print news_array[n]["title"]
        print news_array[n]["news_date"]
        print news_array[n]["url"]