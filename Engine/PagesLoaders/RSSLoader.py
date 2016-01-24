# -*- coding: utf-8 -*-
__author__ = 'popka'



import re
from urllib2 import urlopen
from datetime import datetime, timedelta
from dateutil import tz
import xml.etree.ElementTree as ET
import logging

class RSSLoader:

    def __init__(self):

        self._pages = ["https://roem.ru/rss/roem-all-news.xml", "http://lifenews.ru/xml/feed.xml", "http://www.forbes.ru/newrss.xml", "http://www.vesti.ru/vesti.rss", "http://lenta.ru/rss", "http://ria.ru/export/rss2/index.xml", "https://navalny.com/blog/post.rss", "https://slon.ru/export/all.xml", "https://meduza.io/rss/all", "http://www.vedomosti.ru/rss/news"]
        self._month_dict = {"Jan":"1", "Feb":"2", "Mar":"3", "Apr":"4", "May":"5", "Jun":"6", "Jul":"7", "Aug":"8", "Sep":"9", "Oct":"10", "Nov":"11", "Dec":"12"}

        self._UTC_TIME_ZONE = tz.gettz('Europe/London')
        self._MOSCOW_TIME_ZONE = tz.gettz('Europe/Moscow')
        self._RATE_LIMIT = "[{u'message': u'Rate limit exceeded', u'code': 88}]"


    def _parse_date(self, date):

        """

        :param date: str, дата в формате - "Fri, 04 Dec 2015 14:45:39 +0000"
        :return: str, дата в человеческом, но буржуйском формате, да еще и в Московском часовом поясе
        """
        timezone = date.split("+")[1]
        date = date.replace(",", "")
        date_array = date.split(' ')

        time = date_array[4]
        day = int(date_array[1])
        month = self._month_dict[date_array[2]]
        year = date_array[3]

        date = str(year)+"-"+str(month)+"-"+str(day)+" "+time
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

        if (timezone != "0300"):
            utc_date = date.replace(tzinfo=self._UTC_TIME_ZONE)
            date = utc_date.astimezone(self._MOSCOW_TIME_ZONE)

        # Обрезаем зону
        date = str(date).split("+")[0]

        # Обрезаем секунды
        splited = date.split(":")
        date = splited[0]+":"+splited[1]
        return date


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
                    date = i.find('pubDate').text

                    link, title, date = self._handle_data(url, link, title, date)
                    news_info =  {
                        "title": title,
                        "news_date": date,
                        "url": link,
                        "type": news_type
                    }

                    #if self._get_hours_until_now(date) >= hour:
                    news_array.append(news_info)

            except Exception:
                logging.error("Url:" + url + " hadn't loaded")



        #print "Собрано ", len(news_array), " новостей с RSS"
        return news_array
