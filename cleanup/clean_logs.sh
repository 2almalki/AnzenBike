# ! /bin/bash

clear

echo "Clean up script being run now."

cd /var/log
sudo rm -rf kern.log*
sudo rm -rf syslog*
sudo rm -rf messages*

echo "Clean up script done running!"