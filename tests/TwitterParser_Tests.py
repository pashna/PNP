__author__ = 'popka'

import unittest
from Parsers.TwitterParser import TwitterParser
import random
import dateutil

class TwitterParset_Tests(unittest.TestCase):


    def test_get_domain(self):
        tw_p = TwitterParser()


        self.assertTrue("tass.ru" == tw_p._get_domain("http://tass.ru/i/rss/logo.png"))