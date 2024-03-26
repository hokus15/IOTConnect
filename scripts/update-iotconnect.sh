#!/bin/bash
echo 'Stopping IOTConnect service...'
sudo service iotconnect stop
echo 'done!'
cd /opt/IOTConnect
git fetch --tags
tag=$(git tag -l | tail -n 1)
echo "Updating IOTConnect to ${tag}..."
git reset --hard
git checkout master
git branch --delete latest
git checkout "$tag" -b latest
echo 'done!'
cp iotconnect/logging.live.conf iotconnect/logging.conf
sudo chown -R pi /opt/IOTConnect
sudo systemctl daemon-reload
echo 'Starting IOTConnect service...'
sudo service iotconnect start
echo 'done!'