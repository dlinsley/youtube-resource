#!/usr/bin/env python3
from __future__ import unicode_literals
import yt_dlp
import json
import sys
import os


def get_vid_meta(msg):
    vidmeta = json.loads(msg)
    toReturn = []
    toReturn.append({'name': 'id','value': vidmeta['id']})
    toReturn.append({'name': 'uploader','value': vidmeta.get('uploader')})
    toReturn.append({'name': 'title','value': vidmeta.get('title')})
    toReturn.append({'name': 'duration','value': str(vidmeta.get('duration'))})
    toReturn.append({'name': 'view_count','value': str(vidmeta.get('view_count'))})
    toReturn.append({'name': 'like_count','value': str(vidmeta.get('like_count'))})
    toReturn.append({'name': 'dislike_count','value': str(vidmeta.get('dislike_count'))})
    toReturn.append({'name': 'average_rating','value': str(vidmeta.get('average_rating'))})
    toReturn.append({'name': 'width','value': str(vidmeta.get('width'))})
    toReturn.append({'name': 'height','value': str(vidmeta.get('height'))})
    toReturn.append({'name': 'fps','value': str(vidmeta.get('fps'))})
    toReturn.append({'name': 'ext','value': vidmeta.get('ext')})
    return toReturn

destination_dir_str = sys.argv[1]
resource_config = json.load(sys.stdin)

try:
    os.makedirs(destination_dir_str)
except FileExistsError:
    pass

os.chdir(destination_dir_str)

ydl_opts = {
    'logtostderr': True,
    'ignoreerrors': True,
    'skip_download': False,
    'format': '137+140'
}
if 'skip_download' in resource_config['source']:
    ydl_opts['skip_download'] = resource_config['source']['skip_download']

if 'format_id' in resource_config['source']:
    ydl_opts['format'] = resource_config['source']['format_id']

exit_code = 0
vid_meta = []
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(resource_config['version']['ref'])
    if ydl._download_retcode:
        exit_code = ydl._download_retcode
    vid_meta = get_vid_meta(json.dumps(ydl.sanitize_info(info)))

print(json.dumps({'version': resource_config['version'], 'metadata': vid_meta}))
sys.exit(exit_code)
