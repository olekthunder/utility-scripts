# Utility scripts and some notes

## js-lint-git

Run eslint on your git files. Interface is similar to git diff. Will run only on js files.

```bash
$ js-lint-git --cached
$ # ...
$ js-lint-git HEAD^^
```

## flake-lint-git

Run flake8 only on changed parts of python files

```bash
$ ./flake-lint-git HEAD^^^
```

## run-in-new-tab

Run your command in new tab for your chosen terminal (set `TERMINAL=myawesometerminal` inside script)

Requires **xdotool** to be installed and visible in $PATH

## linux-notes

Some useful or tricky things (maybe not) from my linux experience

## rotate

Rotates image

```bash
$ ./rotate my.img "-90"
```

## mp3tags2utf8

Convert all tags in mp3 files in the directory from cp1251 to utf8

