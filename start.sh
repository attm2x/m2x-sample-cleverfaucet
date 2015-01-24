#!/bin/sh

MODULE1="w1_gpio"
MODULE2="w1_therm"

if lsmod | grep "$MODULE1" && lsmod | grep "$MODULE2" ; then
  echo "$MODULE1 and $MODULE2 are loaded!"
  echo "Running faucet monitor script..."
  python main.py
  exit 0
else
  echo "Loading modules w1_gpio and w1_therm..."
  modprobe w1-gpio
  modprobe w1-therm
  echo "Modules loaded."
  echo "Running faucet monitor script..."
  python main.py
  exit 0
fi

