#!/bin/bash

# Requires mutagen package (mid3iconv) is a part of it
USAGE=$(cat<<-END
Usage: mp3tags2utf8 \e[4mDIRECTORY\e[0m

Convert all tags in mp3 files in \e[4mDIRECTORY\e[0m from cp1251 to utf8
END
)

if [[ "$#" -eq 0 ]]
then
    echo -e "$USAGE"
    exit 1
fi

find $1 -name "*.mp3" -print0 | xargs -0 mid3iconv -e CP1251 -d

