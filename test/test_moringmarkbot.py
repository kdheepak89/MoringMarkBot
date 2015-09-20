import sys
sys.path.append('../')
from nose.tools import *
# from .. import moringmarkbot
from moringmarkbot import *

def test_get_new_post():

    config_path = 'moringmarkbot.conf'

    with open(config_path) as config_file:
        config = json.load(config_file)

    for key in config:
        if config[key] == '':
            logging.info('Getting from environment')
            config[key] = get_from_environ(key)

    moringmarkbot = MoringMarkBot(**config)

    new_post = moringmarkbot.get_new_post()

    assert(new_post is not None)

def test_submit():

    config_path = 'moringmarkbot.conf'

    with open(config_path) as config_file:
        config = json.load(config_file)

    for key in config:
        if config[key] == '':
            logging.info('Getting from environment')
            config[key] = get_from_environ(key)

    moringmarkbot = MoringMarkBot(**config)

    new_post = moringmarkbot.get_new_post()

    try:
        submission_object = moringmarkbot.reddit.submit('bottesting',
                                        '[MoringMark]',
                                        url=str(new_post['url']),
                                        text=None,
                                        captcha=None,
                                        save=False,
                                        send_replies=False)
        submission_object.delete()
        assert(True)
    except:
        raise


