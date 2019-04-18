## Disable beep

```
echo xset -b >> /etc/xprofile
```

## Add keymaps

```
setxkbmap -option grp:alt_shift_toggle -layout us,ru,ua
```

*alt_shift_toggle to toggle layout via Alt+Shift*


## To set screen brightness
```
xbacklight -set 70
```

## To list fonts for language with names
```
fc-list :lang=ru
```

## To generate rsa key pair and copy to clipboard
```
ssh-keygen -t rsa -b 4096 -C "my-awesome-e-mail@mail.com"
xclip -selection clipboard < ~/.ssh/id_rsa.pu
```

## To display battery status
```
acpi
```

## Connect bluetooth headset

[https://wiki.archlinux.org/index.php/Bluetooth_headset](https://wiki.archlinux.org/index.php/Bluetooth_headset)

#### Install: pulseaudio-alsa, pulseaudio-bluetooth, bluez, bluez-libs, bluez-utils

```
$ usermod -a -G lp $USER
$ sudo systemctl start bluetooth
$ bluetoothctl
[bluetooth]# power on
[bluetooth]# agent on
[bluetooth]# default-agent
[bluetooth]# scan on
[bluetooth]# devices
[bluetooth]# pair DEVICE:MAC:ADDR
[bluetooth]# connect DEVICE:MAC:ADDR
[bluetooth]# scan off
[bluetooth]# exit
```

## Automatically switch to newly-connected devices

```
$ sudo echo load-module module-switch-on-connect > /etc/pulse/default.pa
```

## To auto-enable on boot change /etc/bluetooth/main.conf

```
[Policy]
AutoEnable=true
```

## You can pretty print any json via `python -m json.tool`

```
curl http://my.json.api | python -m json.tool
```

# To make linux and windows use same time while dualboot

```
timedatectl set-local-rtc 1 --adjust-system-clock
```

