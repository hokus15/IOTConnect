#!/bin/bash
echo 'Stopping IOTConnect service...'
sudo service iotconnect stop
echo 'done!'
cd /opt/IOTConnect
tag=$(git describe --tags `git rev-list --tags --max-count=1`)
echo "Updating IOTConnect to ${tag}..."
git reset --hard
git checkout master
git branch --delete latest
git checkout "$tag" -b latest
echo 'done!'
cp iotconnect/logging.live.conf iotconnect/logging.conf
sudo systemctl daemon-reload
echo 'Starting IOTConnect service...'
sudo service iotconnect start
echo 'done!'