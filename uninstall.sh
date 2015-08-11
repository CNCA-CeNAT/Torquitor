#!/bin/bash
# CHECK IF THE USER IS ROOT OR HAS ROOT PRIVILEGES
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi


echo ""
echo "Uninstalling Torquitor..."
echo ""
echo -e "Reading Config File: \e[1m\e[32m/etc/torquitor/torquitor.conf"
echo -e "\e[0m"

# WHERE IS APACHE OR NGINX DOCUMENT ROOT

source /etc/torquitor/torquitor.conf

if [[ $TORQUITORHOME == *"torquitor"* ]]
then
	echo "Document Root set to: $TORQUITORHOME"

	echo "UNINSTALING TORQUITOR ...    "

	# DELETING SERVER DIRECTORIES AND FILES
	rm -rfv $TORQUITORHOME
	rm -rfv /etc/torquitor
	rm /etc/init.d/torquitor
	
	echo ""
	echo ""
	echo "DONE"

	VERSION=`cat /proc/version`
	if [[ $VERSION == *"Red Hat"* ]]
	then
		echo "System is a Red Hat"
		echo -n "REMOVING SERVICE ...	"
		chkconfig --del torquitor
		rm /lib/systemd/system/torquitor.service
		systemctl daemon-reload
		echo -e "\e[1m\e[32mOK\e[0m"
	fi

	exit
fi

echo ""
echo -e "\e[1m\e[31mERROR: \e[0mConfig File is corrupted, missing or incorrect."
echo ""

#


