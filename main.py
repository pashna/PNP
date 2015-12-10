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



#This is a basic listener that just prints received tweets to stdout.


def load_tweets(seconds, key_words):
    """
    Качает потоково твиты
    :param seconds: количество секунд, через которые нужно сохранить
    :param key_words: лист ключевых слов
    """
    l = TwitterCollector(seconds)
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track=key_words)



def load_news(sleep_time, iter_to_save):
    newsCollector = NewsCollector(sleep_time=sleep_time, iter_to_save=iter_to_save)
    newsCollector.load_news()



NEWS_CMD = 1
TWITTER_CMD = 2
ERROR_CMD = -1

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
        print "Введите хотя бы один аргумент. news sleep_time iter_to_save или tw save_seconds"
        return (-1,)

    if sys.argv[1] == "news":

        return 1

    if (sys.argv[1] == "tw"):
        return 2

    return (-1,)




if __name__ == '__main__':
    cmd_command = parse_arg()

    if cmd_command == ERROR_CMD:
        pass

    elif cmd_command == NEWS_CMD:
        print "Качаем новости"
        load_news(60, 5)

    elif cmd_command == TWITTER_CMD:

        print "Качаем твиты"
        try:
            key_words = ["tjournal ru", "vc ru"]#, "roem ru", "lifenews ru", "navalny com", "forbes ru", "vesti ru", "lenta ru", "ria ru", "navalny com", "slon ru", "meduza io", "vedomosti ru"]
            load_tweets(40, key_words)

        except Exception as e:
            pass
