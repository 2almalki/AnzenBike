#!/bin/sh

# ensure the script is placed in /ect/rc.local
# paste this line: /yourpath/bin/anzenbike_startup.sh &

sleep 5
xhost +
# clean logs
sudo chmod 777 ~/Desktop/AnzenBike/cleanup/clean_logs.sh
~/Desktop/AnzenBike/cleanup/clean_logs.sh &
# run lidar
chmod 777 ~/Desktop/AnzenBike/Kevin_Integration/Lidar_run.c
~/Desktop/AnzenBike/Kevin_Integration/Lidar_run.c &
# run camera and motor
sudo python ~/Desktop/AnzenBike/Headlight_detection/headlightDetector.py &
# run ultrasonic
sudo python ~/Desktop/AnzenBike/Ultrasonic_VMotor/UltrasonicSensor.py &
# tailight and laser lane
sudo python ~/Desktop/AnzenBike/integrationGPIO/lookupGPIOinUse.py &

# sudo python ~/Desktop/AnzenBike/ultrasonic &
# sudo python ~/Desktop/AnzenBike/camera &
# sudo python /path/for/motorCamera &
# sudo ./pathforLidar &
# sudo python /path/for/GPIOintegration &