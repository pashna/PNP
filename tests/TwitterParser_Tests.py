__author__ = 'popka'

import unittest
from Parsers.TwitterParser import TwitterParser
import random
import dateutil


class TwitterParset_Tests(unittest.TestCase):


    def test_get_domain(self):
        tw_p = TwitterParser()

        print tw_p._get_domain("http://tassru/i/rss/logo.png")
        #self.assertTrue("tass.ru" == tw_p._get_domain("http://tassru/i/rss/logo.png"))