#!/usr/bin/bash

USAGE="USAGE:
    create-arduino-project PROJECT_NAME"

MAKEFILE_CONTENT="ARDUINO_DIR = /usr/share/arduino
ARDUINO_PORT = /dev/ttyUSB0
ARDMK_VENDOR = archlinux-arduino

USER_LIB_PATH = /home/olekthunder/Arduino/libraries
BOARD_TAG = uno

include /usr/share/arduino/Arduino.mk
"

BASE_FILE_CONTENT="void setup() {

}

void loop() {

}
"

if [ -z "$1" ];
then
    echo "$USAGE"
    exit -1
fi


if [ -d $1 ];
then
    echo "Directory $1 already exits"
    exit -1
fi

mkdir $1
echo "$MAKEFILE_CONTENT" > "$1/Makefile"
echo "$BASE_FILE_CONTENT" > "$1/main.ino"

