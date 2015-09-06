"""
Reddit-Tumblr bot
"""

from HTMLParser import HTMLParser
from pytz import timezone

import datetime
import json
import os
import praw
import pytumblr
import random
import time
import traceback


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

class MoringMarkBot(object):
    """
    MoringMarkBot gets posts from MoringMark's tumblr page
    and posts them to Reddit

    MoringMarkBot will post to the following subreddits
        * /r/gravityfalls
        * /r/rickandmorty
    """

    def __init__(self, **kwargs):


        self.config = kwargs

        print('Initializing')
        self.reddit = praw.Reddit(user_agent=self.config['user_agent'])

        self.tumblr = pytumblr.TumblrRestClient(
        self.config['tumblr_api_key_1'],
        self.config['tumblr_api_key_2'],
        self.config['tumblr_api_key_3'],
        self.config['tumblr_api_key_4']
        )

        self.login(self.config['REDDIT_USERNAME'], self.config['REDDIT_PASSWORD'])

    def login(self, REDDIT_USERNAME, REDDIT_PASSWORD):
        """Logs into Reddit and Tumblr"""

        print('Login to reddit')
        self.reddit.login(REDDIT_USERNAME, REDDIT_PASSWORD, disable_warning=True)

        print('Login to tumblr')
        pass

    def is_new_post_exists(self):
        most_recent_post_date = self.tumblr.posts('moringmark')['posts'][0]['date']
        if time.strptime(self.config['last_post_time'], self.config['tumblr_date_format']) < time.strptime(most_recent_post_date, self.config['tumblr_date_format']):
            return(True)
        else:
            return(False)

    def is_post_about(self, check_tag, tags):
        for tag in tags:
            if check_tag in tag:
                return(True)
            else:
                return(False)

    def get_new_post(self):
        """
        Checks for new_post
        returns url and tags if new_post
        else returns False
        """

        if self.is_new_post_exists():
            dictionary = self.tumblr.posts('moringmark')['posts'][0]


            self.config['last_post_time'] = dictionary['date']

            last_post_time = self.config['last_post_time']
            tumblr_date_format = self.config['tumblr_date_format']

            url = dictionary['post_url']

            month_str = time.strptime(last_post_time, tumblr_date_format).tm_mon
            day_str = time.strptime(last_post_time, tumblr_date_format).tm_mday

            title_date_format = '[%B %d]'
            post_time = '['+str(self.config['month_dict'][str(month_str)]) + ' ' + str(day_str) + ']'

            try:
                post_title = dictionary['caption']
                post_title = strip_tags(post_title)
            except:
                post_title = ''

            tags = dictionary['tags']

            return({'url':url, 'tags': tags, 'post_title': post_title, 'post_time': post_time})
        else:
            return(False)

    def submit(self, url, tags, post_title, post_time):
        RICK_AND_MORTY = False
        GRAVITY_FALLS = False
        SPOILER = False

        if self.is_post_about('rick and morty', tags):
            try:
                submission_object = self.reddit.submit('RickAndMorty',
                                            '[MoringMark] '+str(post_time)+' '+post_title,
                                            url=str(url),
                                            text=None,
                                            captcha=None,
                                            save=False,
                                            send_replies=False)

                if self.is_post_about('spoiler', tags):
                    submission_object.mark_as_nsfw()
            except praw.errors.AlreadySubmitted, e:
                print('Error occurred')
                print("Post already submitted")
                pass
            except praw.errors.APIException, e:
                print "\n"
                print "[ERROR]:", e
                print "\n"
                ArithmeticError#blindly handling any exception that gets thrown
                raise
            except Exception, e:
                print "\n"
                print "[ERROR]:", e
                print "blindly handling any error"
                print "\n"
                raise

        if self.is_post_about('gravity falls', tags):
            try:
                submission_object = self.reddit.submit('GravityFalls',
                                            '[MoringMark] '+str(post_time)+' '+post_title,
                                            url=str(url),
                                            text=None,
                                            captcha=None,
                                            save=False,
                                            send_replies=False)

                if self.is_post_about('spoiler', tags):
                    submission_object.mark_as_nsfw()

            except praw.errors.AlreadySubmitted, e:
                print('Error occurred')
                print("Post already submitted")
                pass
            except praw.errors.APIException, e:
                print "\n"
                print "[ERROR]:", e
                print "\n"
                ArithmeticError#blindly handling any exception that gets thrown
                raise
            except Exception, e:
                print "\n"
                print "[ERROR]:", e
                print "blindly handling any error"
                print "\n"
                raise


def get_from_environ(key):
    try:
        return os.environ[key]
    except:
        raise

def main():

    config_path = 'moringmarkbot.conf.example'

    with open(config_path) as config_file:
        config = json.load(config_file)

    for key in config:
        if config[key] == '':
            print('Getting from environment')
            config[key] = get_from_environ(key)

    moringmarkbot = MoringMarkBot(**config)

    while True:
        print('Waiting 1 second')
        time.sleep(1)
        try:
            new_post = moringmarkbot.get_new_post()

            if new_post:
                print('We have a new post here!')
                moringmarkbot.submit(**new_post)
            else:
                print('Post already submitted')

        except Exception:
            raise
            print('Error occurred! %s', traceback.format_exc())


if __name__ == '__main__':
    main()
