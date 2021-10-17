#!/usr/bin/env python3
from __future__ import unicode_literals
import yt_dlp
import json
import sys

def outputFormatter(versions):
    toReturn = []
    for x in versions:
        toReturn.append({'ref': x})
    return json.dumps(toReturn)

class PlaylistLogger(object):
    def __init__(self):
        self.vidlist = []

    def debug(self, msg):
        if msg.startswith('{"'):
            self.process_playlist_json(msg)
            return
        print("[DEBUG] "+msg, file=sys.stderr)
        return

    def warning(self, msg):
        print("[WARN] "+msg, file=sys.stderr)
        return

    def error(self, msg):
        print("[ERROR] "+msg, file=sys.stderr)
        return

    def process_playlist_json(self, msg):
        playlist = json.loads(msg)
        ok = False
        for x in playlist['entries']:
            if not ok:
                # Want to make sure first entry is accessible
                if self.is_ok(x['id']):
                    ok = True
                else:
                    # This entry will be skipped because it is not accessible (yet)
                    continue
            self.vidlist.append(x['id'])
        return

    def count(self):
        return len(self.vidlist)

    def most_recent(self):
        return self.vidlist[0]

    def since_item(self, item):
        indexOfItem = self.vidlist.index(item)
        toReturn = self.vidlist[0:indexOfItem]
        toReturn.reverse()
        return toReturn

    def is_ok(self, item):
        video_output = VideoLogger()
        ydl_opts = {
            'skip_download': True,
            'logger': video_output,
            'forcejson': False,
            'dump_single_json': False,
            'ignoreerrors': True,
            'extract_flat': False,
            'in_playlist': False,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl2:
            ydl2.download([item])
        return video_output.is_ok()


class VideoLogger(object):
    def __init__(self):
        self.ok = True
    def debug(self, msg):
        print("[DEBUG]" +msg, file=sys.stderr)
        return
    def warning(self, msg):
        print("[WARN] "+msg, file=sys.stderr)
        return
    def error(self, msg):
        print("[ERROR] "+msg, file=sys.stderr)
        self.ok = False
        return
    def is_ok(self):
        return self.ok

resource_config = json.load(sys.stdin)

print("Got Config: "+json.dumps(resource_config), file=sys.stderr)

ydl_output = PlaylistLogger()

ydl_opts_playlist = {
    'skip_download': True,
    'logger': ydl_output,
    'forcejson': False,
    'dump_single_json': True,
    'ignoreerrors': True, 
    'extract_flat': True,
    'in_playlist': True,
}

exit_code = 0

with yt_dlp.YoutubeDL(ydl_opts_playlist) as ydl:
    ydl.download([resource_config['source']['playlist']])
    if ydl._download_retcode:
        exit_code = ydl._download_retcode

try:
    if ('version' in resource_config) and ('ref' in resource_config['version']):
        #Getting newer
        currentVer = resource_config['version']['ref']
        print("Returning newer than: " +currentVer, file=sys.stderr)
        newerItems = ydl_output.since_item(currentVer)
        print(outputFormatter(newerItems))
    else:
        #Getting latest
        print("Was not provided a version, returning latest", file=sys.stderr)
        print(json.dumps([{'ref': ydl_output.most_recent()}]))
except TypeError:
    #Get latest
    print(outputFormatter([ydl_output.most_recent()]))

sys.exit(exit_code)