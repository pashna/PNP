# -*- coding: utf-8 -*-
__author__ = 'popka'

import json
import Parsers.TwitterParser as TwitterParser
from datetime import datetime
from tweepy.streaming import StreamListener
import pandas as pd
import csv
import argparse

class TwitterCollector(StreamListener):

    def __init__(self, save_time=2*3600, path="data/twitter"):
        """
        :param save_time: Время, через которое будем сохраняться. В секунах
        """
        self._tw = TwitterParser.TwitterParser()
        self._prev_date = datetime.now()
        self._tweets = []
        self._save_time = save_time
        self.PATH_TO_FILE = path


    def _is_time_to_save (self):
        #news_date = datetime.strptime(self._prev_date, '%Y-%m-%d %H:%M')
        now = datetime.today()
        return float((now-self._prev_date).total_seconds()) > self._save_time


    def _get_filename(self):
        filename = datetime.now().strftime('%Y_%m_%d %H_%M')+".csv"
        filename = self.PATH_TO_FILE + "/" + filename
        return filename


    def _save(self):

        df = pd.DataFrame(self._tweets)
        filename = self._get_filename()
        df.to_csv(filename, sep=",", index=False, encoding="utf-8", quoting=csv.QUOTE_NONNUMERIC)

        self._prev_date = datetime.now()
        self._tweets = []



    def on_data(self, data):

        tweet = self._tw.parse_tweet(data)
        print tweet

        if tweet:
            self._tweets.append(tweet)


        if (self._is_time_to_save()):
            print "Saving..."
            self._save()

        return True

    def on_error(self, status):
        print status
