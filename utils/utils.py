# -*- coding: utf-8 -*-
__author__ = 'popka'

def normalize_url(url):
    """
    Функция приводит url в стандартный вид
    :param url:
    :return:
    """
    url = url.split("?")[0]
    url = url.split("#")[0]
    url = url.replace("//m.", "//")
    url = url.replace("http://", "")
    url = url.replace("https://", "")
    url = url.replace("www.", "")

    if url[-1] == "/":
        url = url[:-1]

    return url