# -*- coding: utf-8 -*-
__author__ = 'popka'

import json
import Parsers.TwitterParser as TwitterParser
from datetime import datetime
from tweepy.streaming import StreamListener
import pandas as pd
import csv
import argparse
import os

class TwitterCollector(StreamListener):

    def __init__(self, path, save_time=2*3600):
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

        folder_name = self.PATH_TO_FILE + datetime.now().strftime('%Y_%m_%d_%H')

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        filename = datetime.now().strftime('%Y_%m_%d_%H_%M')+".csv"
        filename = folder_name + "/" + "tw_" +filename
        return filename



    def _save(self):

        df = pd.DataFrame(self._tweets)
        filename = self._get_filename()

        df.to_csv(filename, sep=",", index=False, encoding="utf-8", quoting=csv.QUOTE_NONNUMERIC)

        self._prev_date = datetime.now()
        self._tweets = []



    def on_data(self, data):

        tweet = self._tw.parse_tweet(data)

        if tweet:
            #print tweet
            self._tweets.append(tweet)


        if (self._is_time_to_save()):
            print datetime.now().strftime('%Y-%m-%d %H:%M') + "  Saving... {} твиттов".format(len(self._tweets))
            self._save()

        return True

    def on_error(self, status):
        print "ERROR STATUS:" + status
