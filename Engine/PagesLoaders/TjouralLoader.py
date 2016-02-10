# -*- coding: utf-8 -*-
__author__ = 'popka'


import lxml.html as html
from urllib2 import urlopen
from datetime import datetime
import logging
from utils.utils import normalize_url

class TJLoader:

    def __init__(self):
        self._news_pages = ["https://tjournal.ru/editorial/page/{}"]#, "https://tjournal.ru/club/news/recent/page/{}"]
        self._month_map = {u"января":"01", u"февраля":"02", u"марта":"03", u"апреля":"04", u"мая":"05", u"июня":"06", u"июля":"07", u"августа":"08", u"сентября":"09", u"октября":"10", u"ноября":"11", u"декабря":"12"}

    def get_news_uri(self, min_index=1, count=1):
        """

        :param min_index: int, индекс страницы, с которой нужно начать поиск
        :param count: int, количество страниц, которые нужно скачать
        :return: list. список ссылок на новости
        """
        links = []
        for news_page in self._news_pages:

            for i in range(count):
                page = html.parse(urlopen(news_page.format(i+min_index)))
                divs = page.getroot().find_class('b-articles__b__title')

                for div in divs:
                    links.append(div.getchildren()[1].get("href"))

        return links


    def _parse_date(self, date):
        date = date.replace(",", "")
        date = date.split(" ")

        converted_date = date[2]
        converted_date +="-"+self._month_map[date[1]]
        converted_date +="-"+date[0]

        converted_date +=" "+date[3]

        return converted_date


    def get_link_info(self, link):
        """

        :param link: str, url страницы с tjournal, для которой нужно собрать информацию
        :return: dict с данными со страницы
        """
        page = html.parse(urlopen(link))
        root = page.getroot()

        # заголовок
        title = root.find_class("b-article__title")
        title = title[0].find("h1").text

        # парсим количество просмотров
        view = root.get_element_by_id("hitsCount").text
        view = view.replace(" ", "")
        view = int(view)

        # Количество комментариев
        comments = root.find_class("b-article__infoline__comments")
        comment = int(comments[0].find("b").text.replace(" ", ""))

        # Теги
        tags = root.find_class("b-article__tags__tag")
        tag_list = []
        for tag in tags:
            tag_list.append(tag.text)

        # Дата
        date = root.find_class("b-article__infoline__date")
        date = self._parse_date(date[0].text)

        # Первоисточник
        source = root.find_class("b-article__link")
        if len(source) != 0:
            source = source[0].getchildren()[0].getchildren()[1].getchildren()[0].text
        else:
            source = None


        news_type = "TJ_P"

        return {
            "url": normalize_url(link),
            "title": title,
            "views": view,
            "comments": comment,
            "tags": tag_list,
            "news_date": date,
            "type": news_type,
            "source": source,
            "load_time": datetime.now().strftime('%Y-%m-%d %H:%M')
        }


    def get_tj_news_info(self, min_index=1, count=1, first_date="2017-01-01", last_date="2010-01-01"):
        """
        :param min_index: int, индекс минимальной страницы, откуда начинаем поиск
        :param count: int, количество страниц, по которым ищем
        :first_date: время первой новости, которую мы скачаем
        :last_date: время последней новости, которую мы скачаем
        :return: dict с данными со страницы
        """
        logging.debug("Tjournal is loading")
        links = self.get_news_uri(min_index=min_index, count=count)
        link_info_list = []
        i = 0

        for link in links:
            link_info = self.get_link_info(link)

            link_info_list.append(link_info)

            i+=1
            if i%10 == 0:
                logging.debug("{} pages was loaded".format(i))

        return link_info_list