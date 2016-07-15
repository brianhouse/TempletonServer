#!/usr/bin/env python3

from housepy import video, config, log

PATH = "/Users/house/Projects/rats/bronx_lab/1467738431_.mov"
PATH = "/Users/house/Projects/rats/bronx_lab/BDMV_5.mov"
# PATH = "/Users/house/Projects/rats/bronx_lab/video-720p-h264.mov"

video_player = video.VideoPlayer(PATH)    
video_player.play()
