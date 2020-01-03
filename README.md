[![Docker Automated Build](https://img.shields.io/docker/cloud/automated/dlinsley/youtube-resource.svg)](https://hub.docker.com/r/dlinsley/youtube-resource/)
[![Docker Build Status](https://img.shields.io/docker/cloud/build/dlinsley/youtube-resource.svg)](https://hub.docker.com/r/dlinsley/youtube-resource/)

# Youtube Resource

Concourse resource to interact with youtube playlists


## Source Configuration

* `playlist`: *Required* The youtube playlist to watch for changes.
* `format_id`: The format of video to fetch.  See (https://github.com/ytdl-org/youtube-dl/blob/master/README.md#format-selection).  Common format ids: `137+140` (1080p .mp4), `136+140` (720p .mp4). Defaults to `137+140`
* `skip_download`: `True` or `False` to skip download. Defaults to `False`


## Example pipeline

This pipeline fetches any new episode from the podlests podcast youtube channel:

```yaml
---
resource_types:
- name: youtube
  type: docker-image
  source:
    repository: dlinsley/youtube-resource
    tag: latest
  check_every: 24h

- name: podlets
  type: youtube
  check_every: 4h
  source:
    playlist: https://www.youtube.com/playlist?list=PL7bmigfV0EqSh-btGOy8BLG3lsF0ylfZ-
    skip_download: False
    format_id: '137+140'

jobs:
- name: get-podlets
  plan:
  - get: podlets
    trigger: true
    version: every
```
