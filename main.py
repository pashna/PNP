# -*- coding: utf-8 -*-
#Import the necessary methods from tweepy library
from tweepy import OAuthHandler
from tweepy import Stream
from Engine.TwitterCollector import TwitterCollector
from Engine.NewsCollector import NewsCollector
import pandas as pd
import numpy as np
import sys
import argparse


#Variables that contains the user credentials to access Twitter API 
access_token = '3712177576-of3jzZ8gNmlPDfPjPyR0Ljw1Ao2IXdTqX9dZGDZ'
access_token_secret = 'Ky7iKwByHNXX3UMfuMhv6UgVx2IhjLo3KmwpsBQz35wtG'
consumer_key = 'BOuuaMDhNhm6yx0rzqK8bMsbI'
consumer_secret = '3DybJwlkXd2vU6R385yLA8yJblYJltLtwojySD9AVs04ShauZ0'


NEWS_CMD = 1
TWITTER_CMD = 2
ERROR_CMD = -1
DEFAULT_NEWS_PATH = "data/news"
DEFAULT_TWITTER_PATH = "data/twitter"


def load_tweets(seconds_to_save, key_words, path):
    """
    Качает потоково твиты
    :param seconds_to_save: количество секунд, через которые нужно сохранить
    :param key_words: лист ключевых слов
    """
    l = TwitterCollector(path=path, save_time=seconds_to_save)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=key_words)



def load_news(sleep_time, iter_to_save, path):
    newsCollector = NewsCollector(sleep_time=sleep_time, iter_to_save=iter_to_save, path=path)
    newsCollector.load_news()


def parse_arg():
    '''
    parser = argparse.ArgumentParser(description='Process some integers.')

    if len(sys.argv) == 1:
        print "Введите хотя бы один аргумент. news sleep_time iter_to_save или tw save_seconds"
        return (-1,)

    parser.add_argument('', metavar='type', type=int, nargs='+',
                   help='news or tw')
    '''

    if len(sys.argv) == 1:
        print "Запускать так:\npython main.py news sleep_time iter_to_save folder_path\nили\ntw save_seconds  folder_path"
        return (-1,)
    try:
        if sys.argv[1] == "news":
            sleep_time = int(sys.argv[2])
            iter_to_save = int(sys.argv[3])

            path = DEFAULT_NEWS_PATH
            if len(sys.argv) == 5:
                path = sys.argv[4]

            return (1, sleep_time, iter_to_save, path)

        if (sys.argv[1] == "tw"):
            seconds_to_save = int(sys.argv[2])

            path = DEFAULT_TWITTER_PATH
            if len(sys.argv) == 4:
                path = sys.argv[3]

            return (2, seconds_to_save, path)
    except IndexError as e:
        print "Запускать так: \npython main.py news sleep_time iter_to_save [folder_path]\nили\npython main.py tw save_seconds  [folder_path]"

    return (-1,)




if __name__ == '__main__':

    """ Очень влом писать нормальный парсер. Потом сделаю, если будет нужно """
    cmd_command = parse_arg()


    if cmd_command[0] == ERROR_CMD:
        pass


    elif cmd_command[0] == NEWS_CMD:
        print "Качаем новости"
        load_news(sleep_time=cmd_command[1], iter_to_save=cmd_command[2], path=cmd_command[3])


    elif cmd_command[0] == TWITTER_CMD:

        print "Качаем твиты"
        while(1):
            try:
                key_words = ["tjournal ru", "vc ru", "roem ru", "lifenews ru", "navalny com", "forbes ru", "vesti ru", "lenta ru", "ria ru", "navalny com", "slon ru", "meduza io", "vedomosti ru"]
                load_tweets(seconds_to_save=cmd_command[1], key_words=key_words, path=cmd_command[2])

            except Exception as e:
                print(e)
