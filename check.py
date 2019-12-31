#!/usr/bin/env python3
from __future__ import unicode_literals
import youtube_dl
import json
import sys

def outputFormatter(versions):
    toReturn = []
    for x in versions:
        toReturn.append({'ref': x})
    return json.dumps(toReturn)

class MyLogger(object):
    def __init__(self):
        self.vidlist = []

    def debug(self, msg):
        if msg.startswith('{"'):
            vid = json.loads(msg)
            self.vidlist.append(vid['id'])

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

    def count(self):
        return len(self.vidlist)

    def most_recent(self):
        return self.vidlist[0]

    def since_item(self, item):
        indexOfItem = self.vidlist.index(item)
        toReturn = self.vidlist[0:indexOfItem]
        toReturn.reverse()
        return toReturn

resource_config = json.load(sys.stdin)

ydl_output = MyLogger()

ydl_opts = {
    'skip_download': True,
    'logger': ydl_output,
    'forcejson': True,
    'ignoreerrors': True,
    'extract_flat': True,
    'in_playlist': True
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([resource_config['source']['playlist']])

try:
    if ('version' in resource_config) and ('ref' in resource_config['version']):
        #Getting newer
        currentVer = resource_config['version']['ref']
        newerItems = ydl_output.since_item(currentVer)
        print(outputFormatter(newerItems))
    else:
        #Getting latest
        print(json.dumps({'ref': ydl_output.most_recent()}))
except TypeError:
    #Get latest
    print(outputFormatter([ydl_output.most_recent()]))
