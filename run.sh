#!/usr/bin/bash

function run {
    if ! pgrep $1 ;
    then
        $@&
    fi
}

function run_terminal {
    commands="$@"
    urxvt -hold -e $SHELL -c "$commands;$SHELL" &
}

run firefox
run_terminal neofetch

