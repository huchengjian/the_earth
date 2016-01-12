#!/usr/bin/env sh

python /Users/hugo/dev/workspace/pycharm_workspace/stuffs/earth/earth.py >> /data/earth_project/x.log

img_path=`cat /data/earth_project/pictures/newest_file`

osascript <<EOF
tell application "Finder" to set desktop picture to POSIX file "$img_path"
EOF
