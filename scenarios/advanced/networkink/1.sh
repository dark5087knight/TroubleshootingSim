#!/bin/bash


echo "---------------------------------------------"
echo -e "
you can not ping google.com why?
do a littil bit search and im sure you will findout what is the problem and solve it
But it's Better if you sreach and and lean about these Concepts
1-Linux NetworkManegar
2-nmcli (command)
3-reslove.conf (file)"
echo "---------------------------------------------"
read -p "If you are ready type 'y', if not type 'n': " CHOICE
if [[ "$CHOICE" == "y" ]]; then
        echo "OK lets goooooo"
    else
        echo "OK See you next time."
        exit
fi

nmcli -t -f NAME,DEVICE,TYPE,STATE con show --active | while IFS=: read -r CON_NAME DEVICE TYPE STATE
do
    [[ "$TYPE" != "802-3-ethernet" && "$TYPE" != "802-11-wireless" ]] && continue

    IPV4_METHOD=$(nmcli -g ipv4.method con show "$CON_NAME" 2>/dev/null)

    if [[ "$IPV4_METHOD" == "manual" ]]; then
        MODE="manual"
    elif [[ "$IPV4_METHOD" == "auto" ]]; then
        MODE="auto"
        nmcli con modify $DEVICE ipv4.ignore-auto-dns yes
    else
        MODE="UNKNOWN ($IPV4_METHOD)"
    fi

    nmcli con modify $DEVICE ipv4.dns "0.0.0.0"
    nmcli connection down $DEVICE > /dev/null
    nmcli connection up $DEVICE  > /dev/null
    nmcli connection reload $DEVICE  > /dev/null
    systemctl restart NetworkManager  > /dev/null

done
reboot