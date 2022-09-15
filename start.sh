#! /bin/bash
# chkconfig: 345 99 20
# description: zw22 start...


export zw22_path="/root/zw22"

export date_day=$(date "+%Y-%m-%d")

export zw22_mongodb_port="3001"
export zw22_pid_mongodb="$zw22_path/server/mongodb.pid"
export zw22_mongodb_exe_log="$zw22_path/logs/server_mongodb_$date_day.log"

export zw22_pid_python="$zw22_path/server/python.pid"
export zw22_python_exe_log="$zw22_path/logs/server_python_$date_day.log"
export zw22_python_py="$zw22_path/server/prisma.py"

export zw22_pid_npm="$zw22_path/server/npm.pid"
export zw22_npm_exe_log="$zw22_path/logs/client_npm_$date_day.log"



echo "----------------------------------"
ps -ef | grep -e prisma.py -e bind_ip -e meteor
echo "----------------------------------"

if [ -f $zw22_pid_mongodb ]; then
	kill -9 `cat $zw22_pid_mongodb`
	echo "Kill Mongodb process!!" 
fi 
echo $zw22_path/server/mongodb/db
echo "mongodb start path  /usr/bin/mongod --dbpath $zw22_path/server/mongodb/db --logpath $zw22_path/server/mongodb/mogodb_log --port $zw22_mongodb_port --bind_ip"
nohup /usr/bin/mongod --dbpath $zw22_path/server/mongodb/db --logpath $zw22_path/server/mongodb/mogodb_log --port $zw22_mongodb_port --bind_ip "localhost" >> $zw22_mongodb_exe_log 2>&1 & echo $! > $zw22_pid_mongodb
#tail $zw22_mongodb_exe_log
echo "*** Start Mongodb process!!" 

if [ -f $zw22_pid_python ]; then
	kill -9 `cat $zw22_pid_python`
	echo "Kill Python process!!" 
fi 

cd $zw22_path/server
nohup python3 $zw22_python_py >> $zw22_python_exe_log 2>&1 & echo $! > $zw22_pid_python
#tail $zw22_python_exe_log
echo "--- Start Python process!!" 

ps -ef | grep meteor | awk '{print $2}' | xargs kill -9

cd $zw22_path/client
nohup npm start  >> $zw22_npm_exe_log 2>&1 & 
echo "=== Start NPM process!!" 


echo "=================================="
ps -ef | grep -e prisma.py -e bind_ip -e meteor
echo "=================================="

