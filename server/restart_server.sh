#! /bin/bash
# chkconfig: 345 99 20
# description: zw22 start...


export dc22_path="/root/dc22"

export date_day=$(date "+%Y-%m-%d")



export dc22_pid_python="$dc22_path/server/python.pid"
export dc22_python_exe_log="$dc22_path/server/logs/server_python_$date_day.log"
export dc22_python_py="$dc22_path/server/prisma.py"



echo "----------------------------------"
ps -ef | grep -e prisma.py
echo "----------------------------------"



if [ -f $dc22_pid_python ]; then
	kill -9 `ps -ef | grep -e py | grep -v grep | awk '{print $2}'`
	echo "Kill Python process!!" 
fi 

cd $dc22_path/server
nohup python3 $dc22_python_py >> $dc22_python_exe_log 2>&1 & echo $! > $dc22_pid_python
#tail $dc22_python_exe_log
echo "--- Start Python process!!" 

echo "=================================="
ps -ef | grep -e prisma.py 
echo "=================================="

tail -f $dc22_python_exe_log

