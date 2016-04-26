#!/usr/bin/python3

from datetime import datetime, timedelta
from lxml import etree
import re
import urllib.request

class LindwurmScraper():
    def __init__( self, url ):
        self.entries = []

        tree = None
        with urllib.request.urlopen( url ) as f:
            tree = etree.HTML( f.read() )
        musics = tree.xpath( "//p/span" )
        for music in musics:
            entry_time = datetime( 1970, 1, 1 )
            line = etree.tounicode( music, method="text" )
            if not '|' in line:
                continue

            m = re.match( "^.+?([0-9\.]+)\s+(.*)$", line )
            if not m:
                continue

            this_year = datetime.now().strftime( "%Y" )
            dt = datetime.strptime( m.group(1) + this_year, "%d.%m.%Y" )
            entry_text = dt.strftime( "%d.%m." ) + " - " + m.group(2)
            entry_url = 'http://www.lindwurm-linden.de/termine/' + entry_text.split()[0]

            self.entries.append( dict( url=entry_url, time=entry_time, title=entry_text, text=entry_text ) )
