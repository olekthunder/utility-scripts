#!/bin/bash

check_inside_git_repository() {
    if [ ! -d ".git" ]; then
        echo -e "\e[41mERROR!\e[49m Not a git repository!"
        exit 1
    fi
}

check_inside_npm_repository() {
    if [ ! -f "package.json" ]; then
        echo -e "\e[41mERROR!\e[49m Not a npm repository!"
        exit 1
    fi
}



check_inside_git_repository
check_inside_npm_repository
for i in $(git diff --name-only $1 \*.js \*.jsx)
do
    npm run eslint "$i"
done

