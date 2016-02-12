# -*- coding: utf-8 -*-
__author__ = 'popka'



import re
from urllib2 import urlopen
from datetime import datetime, timedelta
from dateutil import tz
import xml.etree.ElementTree as ET
import logging
from utils.utils import normalize_url

class RSSLoader:

    def __init__(self):

        self._pages = ["https://roem.ru/rss/roem-all-news.xml",
                       "http://lifenews.ru/xml/feed.xml",
                       "http://www.forbes.ru/newrss.xml",
                       "http://www.vesti.ru/vesti.rss",
                       "http://lenta.ru/rss",
                       "http://ria.ru/export/rss2/index.xml",
                       "https://navalny.com/blog/post.rss",
                       "https://slon.ru/export/all.xml",
                       "https://meduza.io/rss/all",
                       "http://www.vedomosti.ru/rss/news",

                       #========= НОВЫЕ
                       "https://nplus1.ru/rss",
                       "http://tass.ru/rss/export/index.xml?feed=v2",
                       "http://www.interfax.ru/rss.asp",
                       "http://www.ixbt.com/export/news.rss",
                       "http://www.3dnews.ru/news/rss/",
                       "https://www.iphones.ru/feed",
                        "https://www.iguides.ru/rss/main.rss",
                        "http://www.ferra.ru/export/news-rss.xml",
                        "http://www.ferra.ru/export/articles-rss.xml",
                        "http://firrma.ru/data/rss/",
                        "http://rusbase.com/feeds/all/",
                        "http://habrahabr.ru/rss/hubs/all/",
                        "http://geektimes.ru/rss/hubs/all/",
                        "http://megamozg.ru/rss/hubs/all/",
                        "https://tvrain.ru/export/rss/news.xml",
                        "http://www.gazeta.ru/export/rss/first.xml",
                        "http://www.gazeta.ru/export/rss/auto.xml",
                        "http://www.gazeta.ru/export/rss/autonews.xml",
                        "http://www.gazeta.ru/export/rss/business.xml",
                        "http://www.gazeta.ru/export/rss/lastnews.xml",
                        "http://www.gazeta.ru/export/rss/lenta.xml",
                        "http://www.fontanka.ru/fontanka.rss",
                        "http://kp.ru/rss/allsections.xml",
                        "http://www.svoboda.org/api/",
                        "http://izvestia.ru/xml/rss/all.xml",
                        "http://www.novayagazeta.ru/rss/all.xml",
                        "http://polit.ru/feeds/",
                        "http://polit.ru/feeds/article/",
                        "http://polit.ru/feeds/elkin/",
                        "http://www.ntv.ru/exp/newsrss.jsp",
                        #"http://rusplt.ru/news/news.rss",
                        #"http://rusplt.ru/index/new.rss",

                        "http://www.bfm.ru/news.rss",
                        "http://rss.dw.de/xml/rss-ru-all",
                        "http://inosmi.ru/export/rss2/index.xml",
                        "http://feeds.newsru.com/com/www/news/all",

                        "http://regnum.ru/rss/main",
                        "https://russian.rt.com/rss/",

                        "http://bg.ru/export/rss/news.xml",
                        "http://paperpaper.ru/feed/?service",
                        "http://radiovesti.ru/rss/all",
                        "http://www.golos-ameriki.ru/api/",

                        #"http://www.kommersant.ru/RSS/daily.xml",

                        "http://1prime.ru/export/rss2/index.xml",
                        "http://rapsinews.ru/export/rss2/index.xml",

                        "http://apparat.cc/feed/",
                        "http://b2blogger.com/blog/?feed=rss2",
                        "http://www.cossa.ru/rss/",

                        "http://hitech.newsru.com/rss",

                        "http://www.mobile-review.com/rss-review.xml",
                        "http://www.mobile-review.com/rss-material.xml",

                        "http://rusbase.com/feeds/all/",
                        "https://www.iguides.ru/rss/main.rss"
                       ]

        self._month_dict = {"Jan":"1", "Feb":"2", "Mar":"3", "Apr":"4", "May":"5", "Jun":"6", "Jul":"7", "Aug":"8", "Sep":"9", "Oct":"10", "Nov":"11", "Dec":"12"}

        self._UTC_TIME_ZONE = tz.gettz('Europe/London')
        self._MOSCOW_TIME_ZONE = tz.gettz('Europe/Moscow')
        self._RATE_LIMIT = "[{u'message': u'Rate limit exceeded', u'code': 88}]"


    def _parse_date(self, date):

        """

        :param date: str, дата в формате - "Fri, 04 Dec 2015 14:45:39 +0000"
        :return: str, дата в человеческом, но буржуйском формате, да еще и в Московском часовом поясе
        """
        date = re.sub(' +',' ', date)# удаляем лишние пробелы

        if '+' in date:
            timezone = date.split("+")[1]
        else:
            timezone = "0000"

        date = date.replace(",", "")
        date_array = date.split(' ')

        time = date_array[4]
        day = int(date_array[1])
        month = self._month_dict[date_array[2]]
        year = date_array[3]

        date = str(year)+"-"+str(month)+"-"+str(day)+" "+time
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

        if (timezone != "0300"):
            MOSCOW = 3

            hours = timezone[:2]
            hours = int(hours)

            diff_hours = MOSCOW - hours

            if diff_hours > 0:
                date += timedelta(hours=diff_hours)
            else:
                diff_hours = -diff_hours
                date -= timedelta(hours=diff_hours)

            #utc_date = date.replace(tzinfo=self._UTC_TIME_ZONE)
            #date = utc_date.astimezone(self._MOSCOW_TIME_ZONE)

        # Обрезаем зону
        date = str(date).split("+")[0]

        # Обрезаем секунды
        splited = date.split(":")
        date = splited[0]+":"+splited[1]
        return date


    def _handle_link(self, url, link):

        if url == "http://www.3dnews.ru/news/rss/" or \
           url == "http://www.fontanka.ru/fontanka.rss" or \
           url == "http://rss.dw.de/xml/rss-ru-all" or\
           url == "http://bg.ru/export/rss/news.xml" or\
           url == "http://www.ferra.ru/export/news-rss.xml" or\
           url == "http://www.ferra.ru/export/articles-rss.xml":

                link = link.split("?")[0]

            #http://b2blogger.com/ , vesti.ru

        link = link.split("#")[0]

        if link[-1] == "/":
            link = link[:-1]

        return link


    def _get_type(self, url):
        url = url.replace("www.", "")
        url = url.split("://")[1]
        url = url.split("/")[0]
        return url



    def _handle_data(self, url, link, title, date):

        # Убрать лишние пробелы
        title = re.sub(' +',' ', title)

        if url=="https://slon.ru/export/all.xml":
            link = link.split("?")[0]
            title = title.replace("\n", "")

        # Приведение даты к общему формату и временной зоне
        date = self._parse_date(date)
        link = self._handle_link(url, link)

        return link, title, date



    def get_news_array(self):
        """
        hour: int, время последней новости
        """
        news_array = []
        for url in self._pages:
            try:

                news_type = self._get_type(url)
                logging.debug(url + " is loading")

                tree = ET.ElementTree(file=urlopen(url))
                root = tree.getroot()
                for i in root.iter('item'):

                    link = i.find('link').text
                    title = i.find('title').text
                    news_type = self._get_type(link)
                    date = i.find('pubDate').text

                    link, title, date = self._handle_data(url, link, title, date)
                    news_info =  {
                        "title": title,
                        "news_date": date,
                        "url": normalize_url(link),
                        "type": news_type
                    }

                    news_array.append(news_info)

                    #if self._get_hours_until_now(date) >= hour:

            except Exception:
                logging.error("Url:" + url + " hadn't loaded")

        #print "Собрано ", len(news_array), " новостей с RSS"
        return news_array
