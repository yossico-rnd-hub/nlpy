#!env/bin/python

from bs4 import BeautifulSoup
import requests
import lxml.html.clean
import csv
import plac


class Feed(object):
    def __init__(self):
        self.title = ''
        self.url = ''
        self.what = ''
        self.when = ''
        self.where = ''
        self.who = ''
        self.text = ''


@plac.annotations(
    url=("url to read", "option", "n", str))
def main(url=None):
    if url:
        feed = scrape_feed(url)
        print('title:', feed.title)
        print('url:', feed.url)
        print('what:', feed.what)
        print('when:', feed.when)
        print('where:', feed.where)
        print('who:', feed.who)
        print('text:', feed.text)
    else:
        scrape_lapd_news()


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
    text = text.strip('\r\n ')
    text = text.replace('\n', ' ').replace('\r', '')
    bs = BeautifulSoup(text, "lxml")
    return bs.text


def scrape_lapd_news():
    for year in ['2018']:
        for month in ['january']:
            feeds = scrape_news_year_month(year=year, month=month)
    with open('lapd_news.csv', 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(
            ['title', 'url', 'what', 'when', 'where', 'who', 'text'])
        for feed in feeds:
            csv_writer.writerow([
                feed.title,
                feed.url,
                feed.what,
                feed.when,
                feed.where,
                feed.who,
                feed.text])


def scrape_news_year_month(year='2018', month='january'):
    base_url = 'http://www.lapdonline.org'
    source = requests.get('{}/{}_{}'.format(base_url, month, year)).text
    bs = BeautifulSoup(source, 'lxml')

    feeds = []
    for feed_link in bs.find_all(class_='bodylinks'):
        url = '{}{}'.format(base_url, feed_link.attrs['href'])
        feed = scrape_feed(url)
        if not feed.title:
            feed.title = feed_link.text
        feeds.append(feed)
        print(feed.url)
    return feeds


def scrape_feed(url):
    source = requests.get(url).text
    bs = BeautifulSoup(source, 'lxml')

    feed = Feed()
    feed.url = url

    content = bs.find('section', id='content')
    if content:
        h1 = content.find('h1')
        if h1:
            feed.title = h1.text

        for span in content.findChildren('span'):
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

        if ('' == feed.text):
            span = content.find('span')
            if span:
                text = ' '.join(s for s in span.next_siblings
                                if isinstance(s, str) and s != '\n')
                feed.text = clean_text(text)
    return feed


if __name__ == '__main__':
    plac.call(main)
