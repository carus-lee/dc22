#!/bin/bash

if [[ $1 == "start" ]]
then
	systemctl start mongod
	cd /root/dc22/server && nohup python3 prisma.py >> /root/dc22/server/server.log 2>&1 &
	cd /root/dc22/client && nohup npm start >> /root/dc22/client/client.log 2>&1 &
elif [[ $1 == "stop" ]]
then
	kill -9 $(ps -ef | grep -e py | grep -v grep | awk '{print $2}')
	kill -9 $(ps -ef | grep -e node | grep -v grep | awk '{print $2}')
	systemctl stop mongod
fi
