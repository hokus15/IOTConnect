#!/bin/bash

update_app() {
    # Get the latest tag
    latest_tag=$(curl https://api.github.com/repos/$repo/releases/latest | grep \"tag_name\" | cut -d : -f 2,3 | tr -d \", | xargs)
    
    echo "Updating IOTConnect to '${latest_tag}'..."
    
    # Fectch all tags
    git fetch --all --tags --prune
    # Reset
    git reset --hard
    # Check if latest brand exists
    if [ "`git branch --list latest`" ];
    then
        # Move to master to be able to delete 'latest' branch
        git checkout master
        # Delete 'latest' branch
        git branch -D latest;
    fi
    # Checkout latest tag to 'latest' branch
    git checkout tags/"$latest_tag" -b latest

    echo "done!"
}

post_update() {
    echo "Performing post update actions..."
    
    # Change destination dir owner to pi:pi
    sudo chown -R pi:pi "$dest_dir"
    # Allow execution for scripts
    sudo chmod +x "$dest_dir"/scripts/*.sh

    # Update config files
    cp "$dest_dir"/iotconnect/logging.live.conf iotconnect/logging.conf
    cp "$dest_dir"/iotconnect/iotconnect.config.live.json iotconnect.config.json
    sudo cp "$dest_dir"/scripts/*.sh ~
    sudo chown -R pi:pi ~/*.sh
    sudo chmod +x ~/*.sh
    
    echo "done!"
}

repo="hokus15/IOTConnect"
dest_dir="/opt/IOTConnect"

cd "$dest_dir" || exit

echo 'Stopping IOTConnect service...'
sudo service iotconnect stop
echo 'done!'

update_app

post_update

sudo systemctl daemon-reload

echo 'Starting IOTConnect service...'
sudo service iotconnect start

echo 'Update complete!'