# -*- coding: utf-8 -*-
__author__ = 'popka'


import requests
import lxml.html as html
from urllib2 import urlopen
import json
import logging
from datetime import datetime
from utils.utils import normalize_url



class VCLoader:

    def __init__(self):
        self._news_pages = "https://api.vc.ru/1/paper"
        self._month_map = {u"января":"01", u"февраля":"02", u"марта":"03", u"апреля":"04", u"мая":"05", u"июня":"06", u"июля":"07", u"августа":"08", u"сентября":"09", u"октября":"10", u"ноября":"11", u"декабря":"12"}

    def get_news_uri(self, min_index=10, count=30):
        """

        :param min_index: int, индекс страницы, с которой нужно начать поиск
        :param count: int, количество страниц, которые нужно скачать
        :return: list. список ссылок на новости
        """
        links = []
        text = requests.get(self._news_pages).text
        json_req = json.loads(text)

        for news in json_req:
            links.append(news["url"])

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

        :param link: str, url страницы с vc, для которой нужно собрать информацию
        :return: dict с данными со страницы
        """
        page = html.parse(urlopen(link))
        root = page.getroot()

        # заголовок
        title = root.find_class("b-article__head")
        title = title[0].find("h1").text

        # парсим количество просмотров
        view = root.get_element_by_id("hitsCount").text
        view = view.replace(" ", "")
        view = int(view)

        # Количество комментариев
        comments = root.find_class("ccount")[0].text
        comment = int(comments.replace(" ", ""))

        # Теги
        tags = root.find_class("b-tags__tag")
        tag_list = []
        for tag in tags:
            tag_list.append(tag.text)

        # Дата
        date = root.find_class("b-article__infopanel__date")
        date = self._parse_date(date[0].text)


        return {
            "url": normalize_url(link),
            "title": title,
            "views": view,
            "comments": comment,
            "tags": tag_list,
            "news_date": date,
            "type": "VC",
            "load_time": datetime.now().strftime('%Y-%m-%d %H:%M')
        }


    def get_cv_news_info(self, min_index=1, count=1, first_date="2010-01-01", last_date="2017-01-01"):
        """
        :param min_index: int, индекс минимальной страницы, откуда начинаем поиск
        :param count: int, количество страниц, по которым ищем
        :first_date: str, дата и время первой (самой новой) новости
        :last_date: str, дата и время последней(самой старой) новости

        :return: dict с данными со страницы
        """
        logging.debug("VC is loading")
        links = self.get_news_uri(min_index=min_index, count=count)
        link_info_list = []
        i = 0

        for link in links:

            link_info = self.get_link_info(link)
            # Если заданное время не подходит
            #if link_info["date"] > first_date or link_info["date"] < last_date:
            #   continue

            link_info_list.append(link_info)

            i+=1
            if i%10 == 0:
                logging.debug("{} pages was loaded".format(i))

        return link_info_list
