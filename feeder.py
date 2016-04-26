#!/usr/bin/python3

from TwitterScraper import TwitterScraper
from LindwurmScraper import LindwurmScraper
from feedgen.feed import FeedGenerator
import argparse
import sys

class UnsupportedService( NotImplementedError ):
    def __init__( self, *args, **kwargs ):
        Exception.__init__( self, *args, **kwargs )        

class Feeder():
    def __init__( self, url, title='', feedURL='' ):
        scraper = None
        if url.startswith( "https://twitter.com/" ):
            scraper = TwitterScraper( url )
            if title == '':
                title = "Twitter: @" + url.split('/')[3]
        elif url.startswith( "http://www.lindwurm-linden.de/termine" ):
            scraper = LindwurmScraper( url )
            if title == '':
                title = "Lindwurm: Termine"
        else:
            raise UnsupportedService( "No scraper found for this URL." )

        self.feed = FeedGenerator()        
        self.feed.id( url )
        self.feed.title( title )
        self.feed.author( { "name": url } )

        if feedURL != '':
            self.feed.link( href=feedURL, rel='self' )

        for entry in scraper.entries:
            fe = self.feed.add_entry()
            fe.id( entry['url'] )
            fe.title( entry['title'] )
            fe.link( href=entry['url'], rel='alternate' )
            fe.content( entry['text'] )

    def GetAtom( self ):
        return self.feed.atom_str( pretty=True ).decode()


if __name__ == "__main__":
    parser = argparse.ArgumentParser( description="Yet another script to generate Atom feeds from Twitter (and maybe other sites in the future." )
    parser.add_argument( "URL", help="The URL to scrape. URLs of non-supported services will result in an error." )
    args = parser.parse_args()

    try:
        feeder = Feeder( args.URL )
        print( feeder.GetAtom() )
    except UnsupportedService:
        print( "This service is not supported.", file=sys.stderr )
        sys.exit(1)
