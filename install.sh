#!/bin/bash
echo "Installing Torquitor"

# CHECK IF THE USER IS ROOT OR HAS ROOT PRIVILEGES
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# CREATE WORKING DIRECTORIES
mkdir _torquitortmp
tar -xf payload.tar.gz -C _torquitortmp

TMPDIR="payload"
WEBDIR="$TMPDIR/web"

# WHERE IS APACHE OR NGINX DOCUMENT ROOT
echo "Enter the Apache or Nginx Document Root and press ENTER"
echo -n "Leave blank to use default [/var/www/html]: "
DOCROOT=""
read DOCROOT

if [ -z "$DOCROOT" ]; then
	DOCROOT="/var/www/html"
fi

echo "Document Root set to: $DOCROOT"

# CREATE SERVER DIRECTORIES AND FILES
mkdir -p $DOCROOT/torquitor
mkdir -p /etc/torquitor

echo -n "INSTALING TORQUITOR ...    "

# COPY TORQUITOR FILES TO RESPECTIVE LOCATIONS
cp -r $WEBDIR/* $DOCROOT/torquitor/
cp $TMPDIR/torquitor /etc/init.d/
#cp $TMPDIR/torquitor.conf /etc/torquitor/

# CHANGE PERMISSIONS OF TORQUITOR PUBLIC FOLDER TO ENSURE IS VIEWABLE THROUGH WEB
chmod -R a+rx $DOCROOT/torquitor

# CHECK IF SYSTEM IS A REDHAT
# REDHAT SYSTEMS REQUIRE FURTHER CONFIGURATION WHEN INSTALLING SERVICES
VERSION=`cat /proc/version`
if [[ $VERSION == *"Red Hat"* ]]
then
	echo "System is a Red Hat"
	echo -n "INSTALLING SERVICE ...	"
	cp $TMPDIR/torquitor.service /lib/systemd/system/
	chkconfig --add torquitor
	systemctl daemon-reload
	echo -e "\e[1m\e[32mOK\e[0m"
fi

# CREATE THE .CONF FILE IN /etc/torquitor
echo "# Default Config file for TORQUITOR" > /etc/torquitor/torquitor.conf
echo "" >> /etc/torquitor/torquitor.conf
echo "# Set the TORQUITORHOME variable, change this value to the location of your Torquitor directory" >> /etc/torquitor/torquitor.conf
echo "export TORQUITORHOME=$DOCROOT/torquitor" >> /etc/torquitor/torquitor.conf
echo "" >> /etc/torquitor/torquitor.conf
echo "# Set the QSTATHOME variable, change this if qstat is not installed in the default directory. Default is /usr/local/bin
export QSTATHOME=/usr/local/bin

# Set the PBSNODESHOME variable, change this if pbsnodes is not installed in the default directory. Default is /usr/local/bin
export PBSNODESHOME=/usr/local/bin

# Set default icons routes for TORQUITOR web client
# Icons must be stored in TORQUITORHOME or a subfolder
ICONINSTITUTION=gradiente-cenat.png
ICONDEPARTMENT=gradiente-cnca.png

# Set default links to institution and department
URLINSTITUTION=http://www.cenat.ac.cr
URLDEPARTMENT=http://www.cenat.ac.cr/computacion-avanzada/cnca/cnca-resena

# Set default refresh rate for TORQUITOR web client (in seconds)
REFRESHRATE=5" >> /etc/torquitor/torquitor.conf

rm -rf _torquitortmp

echo -e "\e[1m\e[32mDONE\e[0m"

#


