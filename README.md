[![Docker Automated Build](https://img.shields.io/docker/cloud/automated/dlinsley/youtube-resource.svg)](https://hub.docker.com/r/dlinsley/youtube-resource/)
[![Docker Build Status](https://img.shields.io/docker/cloud/build/dlinsley/youtube-resource.svg)](https://hub.docker.com/r/dlinsley/youtube-resource/)

# YouTube Resource

[Concourse](https://github.com/concourse/concourse) resource to interact with youtube playlists


## Source Configuration

* `playlist`: *Required* The youtube playlist to watch for changes.
* `format_id`: The format of video to fetch. See [youtube-dl docs for options](https://github.com/ytdl-org/youtube-dl/blob/master/README.md#format-selection).  
   Common format ids: `137+140` (1080p H.264 w/AAC 128k audio), `136+140` (720p H.264 w/AAC 128k audio). Defaults to `137+140`
* `skip_download`: `True` or `False` to skip the video download. Only metadata of the video will be retrieved if `True`. Defaults to `False`.


### Example pipeline

This pipeline fetches any new episode from the [podlets podcast](https://thepodlets.io/) youtube [channel](https://www.youtube.com/playlist?list=PL7bmigfV0EqSh-btGOy8BLG3lsF0ylfZ-):

```yaml
---
resource_types:
- name: youtube
  type: docker-image
  source:
    repository: dlinsley/youtube-resource
    tag: latest
  check_every: 24h    #prevents querying docker hub every minute

- name: podlets
  type: youtube
  check_every: 4h     #prevents querying youtube every minute
  source:
    playlist: https://www.youtube.com/playlist?list=PL7bmigfV0EqSh-btGOy8BLG3lsF0ylfZ-
    skip_download: False
    format_id: '137+140'

jobs:
- name: get-podlets
  plan:
  - get: podlets
    trigger: true
    version: every   #build for every video if playlist updated with multiple items
```

## Behavior

### `check`: Check for videos added to the head of the playlist
[youtube-dl](https://github.com/ytdl-org/youtube-dl/) is used within the resource to get details about the playlist.  When `check` is executed with no version, the id of the video on the front of the playlist is returned.  If `check` is executed with a version, the ids of all videos newer (towards the beginning of the playlist) are returned.

### `in`: Retrieves the video by id
Retrieves the video using [youtube-dl](https://github.com/ytdl-org/youtube-dl/) based on source config.

### `out`: Not implemented.
