#!/usr/bin/python3

from datetime import datetime
from lxml import etree
import re
import urllib.request

class TwitterScraper():
    def __init__( self, url ):
        self.entries = []

        tree = None
        with urllib.request.urlopen( url ) as f:
            tree = etree.HTML( f.read() )
        tweets = tree.xpath( "//ol/li/div" )
        for tweet in tweets:
            entry_url = ''
            entry_time = None
            times = tweet.xpath( ".//small[@class='time']/a" )
            if len(times) > 0:
                entry_url = "http://twitter.com" + times[0].get( "href" )
                times2 = times[0].xpath( ".//span" )
                if len(times2) > 0:
                    entry_time = datetime.fromtimestamp( float(times2[0].get( "data-time" )) )

            entry_text = ''
            contents = tweet.xpath( ".//div[@class='js-tweet-text-container']/p" )
            if len(contents) > 0:
                s = etree.tounicode( contents[0], method="text" )
                entry_text = re.sub( "\s+", " ", s ).strip()
            entry_title = entry_text
            if len(entry_title) > 100:
                entry_title = entry_text[0:100] + "..."

            self.entries.append( dict( url=entry_url, time=entry_time, title=entry_title, text=entry_text ) )
