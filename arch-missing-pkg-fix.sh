#!/bin/bash

for pkgname in $(sudo pacman -Qk 2>/dev/null | grep "[1-9] missing files" | cut -d ":" -f 1)
do
    yay -S $pkgname --noconfirm 2>/dev/null
done

echo "All packages are fixed"
