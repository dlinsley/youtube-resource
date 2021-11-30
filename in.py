#!/usr/bin/env python3
from __future__ import unicode_literals
import yt_dlp
import json
import sys
import os

class MyLogger(object):
    def __init__(self):
        self.vidmeta = {}

    def debug(self, msg):
        if msg.startswith('{"'):
            self.vidmeta = json.loads(msg)
            return
        print('[DEBUG] '+msg, file=sys.stderr)
        return

    def warning(self, msg):
        print('[WARN] '+msg, file=sys.stderr)
        return

    def error(self, msg):
        print('[ERROR] '+msg, file=sys.stderr)
        return

    def get_vid_meta(self):
        toReturn = []
        toReturn.append({'name': 'id','value': self.vidmeta['id']})
        toReturn.append({'name': 'uploader','value': self.vidmeta.get('uploader')})
        toReturn.append({'name': 'title','value': self.vidmeta.get('title')})
        toReturn.append({'name': 'duration','value': str(self.vidmeta.get('duration'))})
        toReturn.append({'name': 'view_count','value': str(self.vidmeta.get('view_count'))})
        toReturn.append({'name': 'like_count','value': str(self.vidmeta.get('like_count'))})
        toReturn.append({'name': 'dislike_count','value': str(self.vidmeta.get('dislike_count'))})
        toReturn.append({'name': 'average_rating','value': str(self.vidmeta.get('average_rating'))})
        toReturn.append({'name': 'width','value': str(self.vidmeta.get('width'))})
        toReturn.append({'name': 'height','value': str(self.vidmeta.get('height'))})
        toReturn.append({'name': 'fps','value': str(self.vidmeta.get('fps'))})
        toReturn.append({'name': 'ext','value': self.vidmeta.get('ext')})
        return toReturn

destination_dir_str = sys.argv[1]
resource_config = json.load(sys.stdin)

try:
    os.makedirs(destination_dir_str)
except FileExistsError:
    pass

os.chdir(destination_dir_str)

ydl_output = MyLogger()

ydl_opts = {
    'logger': ydl_output,
    'forcejson': True,
    'ignoreerrors': True,
    'skip_download': False,
    'format': '137+140'
}
if 'skip_download' in resource_config['source']:
    ydl_opts['skip_download'] = resource_config['source']['skip_download']

if 'format_id' in resource_config['source']:
    ydl_opts['format'] = resource_config['source']['format_id']

exit_code = 0
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([resource_config['version']['ref']])
    if ydl._download_retcode:
        exit_code = ydl._download_retcode

print(json.dumps({'version': resource_config['version'], 'metadata': ydl_output.get_vid_meta()}))
sys.exit(exit_code)
