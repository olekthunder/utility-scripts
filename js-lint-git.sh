#!/bin/bash

for i in $(git diff --name-only $1 \*.js \*.jsx)
do
    npm run eslint "$i"
done

