# -*- coding: utf-8 -*-
__author__ = 'popka'
from datetime import datetime, timedelta
from dateutil import tz
import json
from utils.utils import normalize_urls


class TwitterParser:

    def __init__(self):
        self._UTC_TIME_ZONE = tz.gettz('Europe/London')
        self._MOSCOW_TIME_ZONE = tz.gettz('Europe/Moscow')

    def _parse_date(self, date):

        """

        :param date: str, дата в формате твиттера - "Sat Nov 21 17:00:29 +0000 2015"
        :return: str, дата в человеческом, но буржуйском формате, да еще и в Московском часовом поясе
        """

        date = datetime.strptime(date,'%a %b %d %H:%M:%S +0000 %Y')
        utc_date = date.replace(tzinfo=self._UTC_TIME_ZONE)
        moscow_date = utc_date.astimezone(self._MOSCOW_TIME_ZONE)

        return str(moscow_date).split("+")[0]


    def _get_tweet(self, data):

        """
        :param data: json string of tweet
        :rtype : json if it is tweet or none else
        """
        tweet = json.loads(data)
        if tweet.get("user"):
            return tweet
        else:
            return None



    def parse_tweet(self, data):

        tweet = self._get_tweet(data)

        if not (tweet):
            return None

        tweet = json.loads(data)

        urls = tweet.get("entities")["urls"]

        if len(urls) == 0:
            link = "NoLink"
        else:
            urls = urls[0]
            link = urls["expanded_url"]

        link = normalize_urls(link)

        user = tweet.get("user")
        if user:
            screen_name = user.get("screen_name")
            followers_count = user.get("followers_count")
            friends_count = user.get("friends_count")
            listed_count = user.get("listed_count")
            user_favourites_count = user.get("favourites_count")
            user_statuses_count = user.get("statuses_count")
            user_id = user.get("id_str")
            user_verified = 1 if user.get("verified") else 0
            user_avatar = user.get("profile_image_url")
            user_date_created = self._parse_date(user.get("created_at"))
            user_location = user.get("location")
            user_timezone = user.get("time_zone")

            user_contributors = user.get("contributors")

            if user_contributors:
                user_contributors = ",".join(str(x) for x in user_contributors)
            else:
                user_contributors = None


            

        created_at = self._parse_date(tweet.get("created_at"))
        tw_id = tweet.get("id")

        if tweet.get("retweeted_status"):
            is_retweet = 1
        else:
            is_retweet = 0


        tw_geo = None if not tweet.get("geo") else tweet.get("geo")
        tw_source = tweet.get("source")


        tw_dict= {
                    "url": link,
                    "tw_id":tw_id,
                    #"retweeted_count": retweeted_count,
                    #"favorite_count":favorite_count,
                    "is_retweet": is_retweet,
                    "created_at":created_at,
                    "tw_geo":tw_geo,
                    "tw_source": tw_source,
                    "user_id": user_id,
                    "screen_name": screen_name,
                    "user_followers_count":followers_count,
                    "user_listed_count": listed_count,
                    "user_friends_count":friends_count,
                    "user_favourites_count":user_favourites_count,
                    "user_statuses_count": user_statuses_count,
                    "user_verified":user_verified,
                    "user_avatar":user_avatar,
                    "user_date_created":user_date_created,
                    "user_location": user_location,
                    "user_timezone": user_timezone,
                    "user_contributors":user_contributors
                    }

        return tw_dict




"""
tw_dict= {
        "url": link,
        "tw_id":tw_id,
        "retweeted_count": retweeted_count,
        "favorite_count":favorite_count,
        "is_retweet": is_retweet,
        "created_at":created_at,
        "user_followers_count":followers_count,
        "user_listed_count": listed_count,
        "user_friends_count":friends_count,
        "user_favourites_count":favourites_count,
        "user_statuses_count":statuses_count
        }
"""