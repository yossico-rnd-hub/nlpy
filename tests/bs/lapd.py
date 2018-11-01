#!env/bin/python

from bs4 import BeautifulSoup
import requests


class Feed(object):
    def __init__(self):
        self.title = ''
        self.url = ''
        self.what = ''
        self.when = ''
        self.where = ''
        self.who = ''
        self.text = ''


def get_text(span):
    text = None
    if isinstance(span.next_sibling, str):
        text = span.next_sibling
    elif isinstance(span.next_sibling.next_sibling, str):
        text = span.next_sibling.next_sibling
    if text:
        return clean_text(text)
    return 'scraping error!'


def clean_text(text):
    text = text.strip('\n')
    return text


def scrape_lapd_news():
    for year in ['2018']:
        for month in ['january']:
            feeds = scrape_news(year=year, month=month)


def scrape_news(year='2018', month='january'):
    base_url = 'http://www.lapdonline.org'
    source = requests.get('{}/{}_{}'.format(base_url, month, year)).text
    soup = BeautifulSoup(source, 'lxml')

    feeds = []
    for feed in soup.find_all(class_='bodylinks'):
        title = feed.text
        url = '{}{}'.format(base_url, feed.attrs['href'])
        feed = scrape_feed(url)
        feed.title = title
        feed.url = url
        feeds.append(feed)
        print(feed.url)
    return feeds


def scrape_feed(feed_url):
    source = requests.get(feed_url).text
    soup = BeautifulSoup(source, 'lxml')
    # div = soup.find('div', class_='row-fluid')

    feed = Feed()
    for span in soup.find_all('span'):
        if span.text == 'WHAT:':
            feed.what = get_text(span)
            continue
        if span.text == 'WHEN:':
            feed.when = get_text(span)
            continue
        if span.text == 'WHERE:':
            feed.where = get_text(span)
            continue
        if span.text == 'WHO:':
            feed.who = get_text(span)
            continue
        if span.text == 'WHY:':
            feed.text = get_text(span)
            continue

    return feed


if __name__ == '__main__':
    scrape_lapd_news()
