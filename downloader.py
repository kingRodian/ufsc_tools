#!/usr/bin/env python

"""
downloader.py
You have to register an APP with twitter to get tokens for use with the program.
I have encrypted my own secret tokens, and use gpg with a passphrase to decrypt it.

If given, the program reads a json file which details the ids of tweets have been checked, and it retrieves tweets
from that point to the present.
If there is no such file provided, it starts from the beginning.
(the furthest back one can go is 3200, I think, which means we cannot get all the ufsc vids).

"""


import argparse
from collections import OrderedDict
from getpass import getpass
import gnupg
import json
import logging
import logging.handlers
import os
import time
import tweepy
from tweepy import OAuthHandler
import wget





class Downloader:
    def __init__(self, tokens, target_username, conf_path, progress_file, target_directory, logger):
        self.auth = OAuthHandler(tokens['consumer_key'], tokens['consumer_secret'])
        self.auth.set_access_token(tokens['access_token'], tokens['access_secret'])
        self.target_username = target_username
        self.conf_path = conf_path
        self.progress_file = progress_file
        self.target_directory = target_directory
        self.logger = logger
        self.twitter_api = tweepy.API(self.auth)
        self.logger.info('Authorized. Checking progress...')

        # See if there is a file describing the progress which we can use
        self.filelist = set(os.listdir())
        self._check_progress()

    def _check_progress(self):
        # If no json file
        if self.progress_file not in self.filelist:
            self.visited_ids = OrderedDict({})
            self.lastid = None
        else:
            with open(self.conf_path + self.progress_file, 'r') as f:
                self.visited_ids = OrderedDict(json.load(f))
                self.lastid = next(reversed(self.visited_ids))

    def _handle_limit(self, cursor):
        while True:
            try:
                yield cursor.next()
            except tweepy.RateLimitError:
                self.logger.warning('Rate limit reached, sleeping...')
                # Respect the limit
                time.sleep(15 * 60)

    def _get_tweets(self):
        tweets = []
        if self.lastid:
            self.logger.info('Getting tweets after id: {}...'.format(self.lastid))
            tweets = [tweet for tweet in self._handle_limit(tweepy.Cursor(self.twitter_api.user_timeline,
                id=self.target_username, since_id=int(self.lastid)).items())]
        else:
            self.logger.info('Getting tweets from beginning...')
            tweets = [ tweet for tweet in self._handle_limit(tweepy.Cursor(self.twitter_api.user_timeline, id = self.target_username).items())]
        return tweets

    def _write_progress(self, ident, filename, status):
        self.visited_ids[ident] = {'filename':filename, 'status':status}
        with open(self.conf_path + self.progress_file, 'w') as f:
            json.dump(self.visited_ids, f, indent=4)

    def download(self):
        tweets = self._get_tweets()
        # And we want it in chronological order
        tweets.reverse()
        self.logger.info('Tweets found: {}'.format(len(tweets)))
        for tweet in tweets:
            self.lastid = tweet.id
            self.logger.info('Checking status with ID: {}.'.format(self.lastid))
            # The video is always in extended entities because of the thumbnail which comes first
            if not hasattr(tweet, 'extended_entities'):
                self.logger.info('Nothing found, continuing...')
                self._write_progress(self.lastid, '', 'NONE')
                continue
            media = tweet.extended_entities['media'][0]
            # No video, something else
            if not media['type'] == 'video':
                self.logger.info('Nothing found, continuing...')
                self._write_progress(self.lastid, '', 'NONE')
                continue

            urls = [variant['url'] for variant in media['video_info']['variants']]
            url = ''
            # We can get several links, we only want the /vid/
            for link in urls:
                if '/vid/' in link:
                    url = link
                    break
            if not url:
                self.logger.info('Nothing found, continuing...')
                self._write_progress(self.lastid, '', 'NONE')
                continue
            text = tweet.text
            # Get rid of link and the annoying spaces
            name = text[ : text.find(' http')].replace(' ', '')
            extension = url[url.rfind('.') : ]
            filename = name + extension
            self.logger.info('Downloading: {}.'.format(filename))
            if filename not in self.filelist:
                try:
                    wget.download(url, out= self.target_directory + filename)
                    print()
                except Exception as e:
                    self.logger.error('Could not download {}.\nException: {}. Skipping...'.format(url, e))
                    self._write_progress(self.lastid, filename, 'ERROR')
                    continue
                self._write_progress(self.lastid, filename, 'DOWNLOADED')
                self.logger.info('Next..')


def get_tokens(tokenpath, gpg, passphrase):
    tokens = dict()
    with open(tokenpath + 'consumer.key', 'r') as f:
        consumer_key = f.read().strip()
        tokens['consumer_key'] = consumer_key
    with open(tokenpath + 'consumer.secret', 'rb') as f:
        consumer_secret = gpg.decrypt_file(f, passphrase=passphrase).data.decode().strip()
        tokens['consumer_secret'] = consumer_secret
    with open(tokenpath + 'access.token', 'r') as f:
        access_token = f.read().strip()
        tokens['access_token'] = access_token
    with open(tokenpath + 'access.secret', 'rb') as f:
        access_secret = gpg.decrypt_file(f, passphrase=passphrase).data.decode().strip()
        tokens['access_secret'] = access_secret
    return tokens

def main():
    # Command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--gpghome', default='/home/king/.gnupg', type=str, nargs='?',
            help='Path to gpg home.')
    parser.add_argument('-c', '--conf_path', default='/home/king/arg/unfavorablesemicircle/twitter/scripts/', type=str, nargs='?',
            help='Path to config, logs and tokens used for authentication.')
    parser.add_argument('-u', '--username', default='unfavorablesemi', type=str, nargs='?',
            help='Twitter username from which we download videos.')
    parser.add_argument('-p', '--progress_file', default='progress_unfavorablesemi', type=str, nargs='?',
            help='File which keeps track of the latest id')
    parser.add_argument('-t', '--target_directory', default='/home/king/arg/unfavorablesemicircle/twitter/video/', type=str, nargs='?',
            help='Path to target video directory.')
    parser.add_argument('-l', '--logfile', default='downloader.log', type=str, nargs='?',
            help='File to which we log.')
    args = parser.parse_args()

    # Set up logging
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    log_formatter = logging.Formatter('{asctime} - {levelname} - {message}', style='{')
    log_filehandler = logging.handlers.TimedRotatingFileHandler(args.conf_path + args.logfile, when='D')
    log_filehandler.setFormatter(log_formatter)
    log_filehandler.setLevel(logging.DEBUG)
    logger.addHandler(log_filehandler)
    log_streamhandler = logging.StreamHandler()
    log_streamhandler.setFormatter(log_formatter)
    log_streamhandler.setLevel(logging.INFO)
    logger.addHandler(log_streamhandler)



    # Get the password safely
    passphrase = getpass(prompt='GPG Passphrase:')
    gpg = gnupg.GPG(gnupghome=args.gpghome)
    tokens = get_tokens(args.conf_path, gpg, passphrase)
    logger.info('Decrypted tokens(dunno if it worked).')

    downloader = Downloader(tokens, args.username, args.conf_path, args.progress_file, args.target_directory, logger)
    downloader.download()

if __name__ == '__main__':
    main()
