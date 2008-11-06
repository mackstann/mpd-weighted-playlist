#!/usr/bin/env python

import os

artist = os.popen('mpc --format %artist%').readline().rstrip('\n')
album  = os.popen('mpc --format %album%' ).readline().rstrip('\n')
title  = os.popen('mpc --format %title%' ).readline().rstrip('\n')

f = file(os.path.expanduser('~/.mpd-weights'), 'a')

# use repr to make sure any weird characters that have meaning to python get
# escaped properly

print >>f, repr((artist, album, title))+': 0,'

