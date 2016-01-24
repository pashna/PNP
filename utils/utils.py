# -*- coding: utf-8 -*-
__author__ = 'popka'

def handle_link(url):
    """
    Функция приводит url в стандартный вид
    :param url:
    :return:
    """
    if "b2blogger.com" not in url and "vesti.ru" not in url:
        url = url.split("?")[0]

    url = url.split("#")[0]

    if url[-1] == "/":
        url = url[:-1]

    return url
