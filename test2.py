# coding=utf-8
from pymongo import MongoClient
import feedparser
import time
from urlparse import urlparse
import argparse
import codecs
import unidecode


def to_ascii(text):
    return unidecode.unidecode(text).lower().strip()


def get_last_interaction():
    last_interaction = list(db.interaction.find({}).sort('$natural', -1).limit(1))
    if last_interaction:
        last_interaction = last_interaction[0]
    return last_interaction


def feed_to_interaction(entry):
    parsed_url = urlparse(entry.link)
    interaction = {
        'created_at': entry.published,
        'interaction': {
            'interaction': {
                'content_orig': entry.description,
                'author': {
                    'name': parsed_url.netloc,
                    'username': parsed_url.netloc,
                    'link': entry.link
                },
            },
        },
        'content': u'Posted on {} : {}'.format(parsed_url.netloc, entry.description),
        'title': entry.title,
        'type': 'rss_feed',
        'link': entry.link,
        'rss_feed': {
            'from': {
                'name': parsed_url.netloc
            },
        },
    }
    return interaction


def run(entries, keys):
    for entry in entries:
        date = time.strftime("%Y-%m-%d %H:%M:%S", entry.published_parsed)
        entry.published = date
        string_to_find = {entry.title + " " + entry.description}
        last_interaction = get_last_interaction()
        if not last_interaction or last_interaction["created_at"] < entry.published:
            for key in keys:
                for string in string_to_find:
                    if key in to_ascii(string):
                        result = feed_to_interaction(entry)
                        db.interaction.insert(result)


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='Rss feed data source')
    arg_parser.add_argument('--feeds', nargs='*', type=str)
    arg_parser.add_argument('--feeds-from-file', type=str, default=None)
    arg_parser.add_argument('--feeds-from-db', action='store_true', default=False)
    arg_parser.add_argument('--db-uri', type=str, default=None)
    args = arg_parser.parse_args()
    entries = []
    client = MongoClient('172.17.0.1', 27017)
    db = client.rss
    with open("/var/lib/rss/rssKeysList.txt") as f:
        keys = f.read().split(",")
    if args.feeds_from_file:
        with codecs.open(args.feeds_from_file, mode='r', encoding='utf-8') as f:
            feeds = [feed for feed in f.read().split(",")]
    elif args.feeds:
        feeds = args.feeds
    for feed in feeds:
        d = feedparser.parse(feed)
        if "published_parsed" in d.entries[0]:
            entries.extend(d.entries)
        else:
            pass
    entries = sorted(entries, key=lambda k: k.published_parsed)
    run(entries, keys)





