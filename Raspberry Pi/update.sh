#!/bin/bash

echo "Update script by Jun Hao"
echo "Updating Raspberry Pi"
echo press CTRL+C to quit
echo press ENTER to start
read reply
sudo apt-get update
sudo apt-get -y upgrade
sudo apt-get autoremove
sudo apt-get autoclean
echo -e "\n\nAll up to date now!"
echo press Enter to reboot
echo press CTRL+C to cancel reboot
read reply
reboot