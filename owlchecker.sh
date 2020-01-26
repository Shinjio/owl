#!/bin/bash

if pgrep -x "client.py" > /dev/null
then
	echo "1"
else
	/usr/bin/python3 /opt/owl/client.py
fi
