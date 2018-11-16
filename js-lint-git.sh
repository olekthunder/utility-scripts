for i in $(git diff --name-only $1 \*.js \*.jsx)
do
    echo $i
    npm run eslint "$i"
done

