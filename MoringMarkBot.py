
# coding: utf-8

# #MoringMarkBot

from IPython.display import display
from IPython.display import Image
import praw
import time
from config import *

# Testing - Get avatar
Image(url=client.avatar('moringmark')['avatar_url'])

last_post_time = client.posts('moringmark')['posts'][0]['date']
tumblr_date_format = '%Y-%m-%d %H:%M:%S %Z'

# # Check last post time

if time.strptime(last_post_time, tumblr_date_format) > time.strptime(client.posts('moringmark')['posts'][0]['date'], tumblr_date_format):
    last_post_time = client.posts('moringmark')['posts'][0]['date']
    post_url = client.posts('moringmark')['posts'][0]['post_url']

for photo in client.posts('moringmark')['posts'][0]['photos']:
    display(Image(photo['original_size']['url']))


# # Post to Reddit

user_agent = BOT_NAME
r = praw.Reddit(user_agent=user_agent)
r.login(REDDIT_USERNAME, REDDIT_PASS)
r.submit('GravityFalls', '[MoringMark] '+str(last_post_time), url=str(post_url))



