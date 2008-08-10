#!/usr/bin/env python

# Written by Nick Welch in the year 2008.  Author disclaims copyright.

# The mpdclient3 Python module is required.  On Ubuntu the necessary package is
# python-mpdclient.

# This script is for MPD (http://musicpd.org) users who basically like to
# listen to their entire music collection at random, but want a little control
# to play some things more and some things less (and maybe some things not at
# all).

# Unfortunately, by clearing and then filling your playlist, the song currently
# playing will stop abruptly and a new song will start playing. Due to the
# slightly random nature of this script, I like to run it regularly to make
# sure all of my songs get an equal chance, so I create a cron job to run it
# when I'm asleep or gone.  I use a cool utility called xprintidle (you can
# apt-get install it) to check when the computer has been idle for about 4
# hours.  Here's what the cron job looks like:

# @hourly export DISPLAY=:0; test `xprintidle` -gt $((1000*60*60*4)) && python path/to/this/script.py

# Just run crontab -e, which will start an editor, then add that line, save,
# and quit.

# Back on topic.. edit the weights below.

weights = {
    # Notes for non-programmers or non-Python programmers:
    # - Remember to put a comma at the end of each one.
    # - Double quotes and single quotes are equivalent.  Use what's convenient.
    # - To put a double quote in a double-quoted string, you must put a
    #   backslash (\) before it, and the same goes for single quotes.  Like:
    #   'It\'s'.

    # How the weights work:
    # A weight of 2.5 means each song will appear twice and on average 50% of
    # them will appear 3 times. i.e. 2.5x, or 250% of normal.  A weight of .33
    # means that roughly only a third of the files that match that entry will
    # appear at all, and none will appear more than once.  Every file that
    # doesn't match one of the weights you enter here will have a default
    # weight of 1, meaning it will appear once in the playlist.

    # If multiple weights match a single song, like artist and artist+title,
    # then the weights are multiplied by each other.

    # These are case insensitive and no regular expressions or wildcards are
    # implemented.

    # Valid examples (delete them and enter your own here):

    'Some Artist': 1.5,
    ('An Artist', "Hey It's An Album"): 5.0,
    ('Artist', 'Album', 'the name of the song that I hate'): 0,

}

import mpdclient3, re, random

c = mpdclient3.connect()

songs = filter(lambda x: x.type == 'file', c.do.listallinfo())

wasplaying = c.do.status().state == 'play'

c.do.clear()

for song in songs:
    weight = 1
    keys = [
        song.artist, (song.artist, song.album),
        (song.artist, song.album, song.title),
    ]
    for key in keys:
        weight *= weights.get(key, 1)

    this_song_count = int(weight) + int(bool(random.random() < weight % 1))

    print "weight %0.2f, adding %d times: %s" % \
        (weight, this_song_count, song.file)

    for i in range(this_song_count):
        c.do.add(song.file)

if wasplaying:
    c.do.play()

