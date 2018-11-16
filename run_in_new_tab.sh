#!/bin/bash

TERMINAL="gnome-terminal"

# if last command is unsuccessful
if [ pgrep -u "$USER" "$TERMINAL" ]; then
    /usr/bin/$TERMINAL
    sleep 2
    WID=`xdotool search --class "$TERMINAL" | head -1`
    # Runs command given as first argument in new tab of terminal
    xdotool windowfocus $WID
    sleep .1
fi


run_in_new_tab() {
    # Runs command given as first argument in new tab of terminal
    xdotool key ctrl+shift+t
    sleep .2
    for arg in "$@"
    do
        xdotool type --delay .1 "$arg"
        xdotool key Return
        sleep .2
    done
}

run_in_new_tab "echo lol" "echo keke"

