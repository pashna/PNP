# -*- coding: utf-8 -*-
__author__ = 'popka'
from Engine.PagesLoaders.TjouralLoader import TJLoader
from Engine.PagesLoaders.VCLoader import VCLoader
from Engine.PagesLoaders.RSSLoader import RSSLoader
from datetime import datetime
import pandas as pd
import numpy as np
import csv
import time
import os


NEWS_FORMAT = {
    "url": "url",
    "title": "title",
    "date": "news_date",
    "comments": "comments",
    "views": "views",
    "tags": "tags",
    "news_date": "news_date",
    "type": "type"
}

class NewsCollector:


    def __init__(self, path, sleep_time=60*60, iter_to_save=10):
        self._tj_loader = TJLoader()
        self._vc_loader = VCLoader()
        self._rss_loader = RSSLoader()
        self._sleep_time = sleep_time
        self.PATH_TO_FILE = path
        self._iter_to_save = iter_to_save


    def load_new_news(self):
        print "Сейчас " + datetime.now().strftime('%Y-%m-%d %H:%M')

        pages = self._tj_loader.get_tj_news_info()
        pages += self._vc_loader.get_cv_news_info()
        pages += self._rss_loader.get_news_array()

        print "Скачали {} новостей".format(len(pages))

        return pages


    def _drop_duplicates(self, df):
        last_size = len(df)
        dupl = df["url"].duplicated()
        dupl = np.invert((dupl.as_matrix()))
        df = df[dupl]
        #print "Удалено ", last_size-len(df)
        return df


    def _get_filename(self):

        folder_name = self.PATH_TO_FILE + datetime.now().strftime('%Y_%m_%d_%H')

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        filename = datetime.now().strftime('%Y_%m_%d_%H_%M')+".csv"
        filename = folder_name + "/" + "news_" +filename
        return filename



    def _filter_date(self, df):
        """
        Удаляет новости, которые были опубликованы до начала сбора информации
        :param df:
        :return:
        """
        print self._start_date
        df = df[df["news_date"]>= self._start_date]
        return df


    def _prepare_to_save(self, df):
        df = self._filter_date(df)
        df = self._drop_duplicates(df)
        return df


    def load_news(self):

        is_empty_dataframe = True
        iter = 0
        self._start_date = datetime.now().strftime('%Y-%m-%d %H:%M')

        while True:


            print "Спим {} секунд".format(self._sleep_time)
            time.sleep(self._sleep_time)

            pages = self.load_new_news()

            if is_empty_dataframe:
                df = pd.DataFrame(pages)
                is_empty_dataframe = False
            else:
                df = df.append(pd.DataFrame(pages))

            iter += 1

            if iter%self._iter_to_save == 0:

                df = self._prepare_to_save(df)
                print "Saving... {} news".format(len(df))
                df.to_csv(self._get_filename(), sep=",", index=False, encoding="utf-8", quoting=csv.QUOTE_NONNUMERIC)

                is_empty_dataframe = True
                self._start_date = datetime.now().strftime('%Y-%m-%d %H:%M')
