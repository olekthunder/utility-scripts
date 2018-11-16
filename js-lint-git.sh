#!/bin/bash


check_installed() {
    for arg in "$@"
    do
        if [ ! "$(which "$arg")" ]; then
            echo -e "\e[41mERROR!\e[49m \e[1m$arg\e[21m is not installed. Install it via your system package manager"
            exit 1
        fi
    done
}


check_inside_npm_repository() {
    if [ ! -f "package.json" ]; then
        echo -e "\e[41mERROR!\e[49m Not a npm repository!"
        exit 1
    fi
}


main() {
    for i in $(git diff --name-only $1 \*.js \*.jsx)
    do
        npm run eslint "$i"
    done
}


check_inside_npm_repository
check_installed "eslint"

