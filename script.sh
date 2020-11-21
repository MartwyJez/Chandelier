#!/bin/bash

# /etc/init.d/script.sh
### BEGIN INIT INFO
# Provides:          script.sh
# Required-Start:    $all
# Required-Stop:     $all
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start daemon at boot time
# Description:       Enable service provided by daemon.
### END INIT INFO

#check if user is in lp groups
#start and enable bluetoothctl, pulseaudio <as user>, sshd
#automaticly connect to wifi with static ip (from env)
#reboot if exit with error code 10
#
RC=0
SH=0
TSH=0
pushd /home/pi/Chandelier

date
while [[ ${RC} == '0'  ]]; do
  echo "Starting"
  python3 -m chandelier
  RC=$?
  echo $RC
  if [[ ${RC} == '14' ]]; then
    SH==$(($SH + 1))
    RC=0
  elif [[ ${RC} == '0' ]]; then
    echo "Waiting"
    python3 -m chandelier --wait
  else
    echo "Smth happened"
    TSH==$(($SH + 1))
    sleep 2
  fi
  
  if [[ $SH == '3' ]]; then
    echo "Shit happened 3 times in a row, rebooting"
    sudo reboot -f
  fi
  if [[ $TSH == '10' ]]; then
    echo "Total shit happened 10 times in a row, rebooting"
    sudo reboot -f
  fi
  
done
echo "Done $RC"
