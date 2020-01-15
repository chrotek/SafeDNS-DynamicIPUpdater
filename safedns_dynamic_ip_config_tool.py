##!/usr/bin/env bash
#
#printf "Welcome to the SafeDNS Dynamic IP Config Tooln"
#
#showmainmenu () {
#printf "nWhat do you want to do?n
#1) Initial Setup
#2) Add a new Domain
#3) Remove a Domain
#4) Manage API Keys
#
#Type a number and press ENTER , or Press CTRL + C to exit : "
#read OPTION
#
#case "$OPTION" in
#1)
#printf "--- Initial Setup ---n"
#;;
#2)
#printf "--- Add a new Domain ---n"
#;;
#3)
#printf "--- Remove a Domain ---n"
#;;
#
#4)
#printf "--- Manage API Keys ---"
#;;
#?) printf "nUnknown Option!"
#showmainmenu
#;;
#
#
#esac
#morechangesconfirmation
#}
#
#morechangesconfirmation () {
#
#printf "nDo you want to make any other changes? (y/N)nType y or n and press ENTER: "
#RERUN_CONFIRMATION=n
#read -t 10 RERUN_CONFIRMATION
#if [ $? -gt 128 ]
#then
#printf "nTimed out, Exiting"
#fi
#
#case "$RERUN_CONFIRMATION" in
#y|Y)
#showmainmenu
#;;
#n|N)
#exit 0
#;;
#?) printf "nUnknown Option!"
#morechangesconfirmation
#;;
#esac
#}
#
#showmainmenu
