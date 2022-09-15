#!/bin/bash

# 순서

# 1. sub priority 낮춤
# 2. main priority 높임
# 3. main proc 없어질때까지 기다림
# 4. sub priority 원복



export proc_sub="liveTranscoder"
export proc_main="flashextractor"
export proc_main2="Xvfb"

export ni_low="10"
export ni_high="-20"
export ni_normal="0"


function wait_finish(){
        export proc_name=$1
        export wc_proc=$(ps -ef | grep $proc_name | grep -Ev 'grep|tail' | wc -l)

        export dNow="$(date '+%Y%m%d_%H%M%S_')"

        echo "$dNow wait $proc_name $wc_proc"
        while [ "$wc_proc" -gt 0 ]
        do
                export dNow="$(date '+%Y%m%d_%H%M%S_')"

                echo "$dNow wait $proc_name $wc_proc"
                sleep 1
                export wc_proc=$(ps -ef | grep $proc_name | grep -Ev 'grep|tail' | wc -l)
        done

        export dNow="$(date '+%Y%m%d_%H%M%S_')"
        echo "$dNow end $proc_name"



}

function renice_proc(){
        export proc_name=$1
        export val_priority=$2


        export ni_pid=$(ps -ef | grep $proc_name | grep -Ev 'grep|tail' | awk '{print $2}')

        for i in $ni_pid
        do
                renice $val_priority $i
        done

}

# 메인 실행 부분

while :
do
        export dNow="$(date '+%Y%m%d_%H%M%S_')"
        export wc_main=$(ps -ef | grep $proc_main | grep -Ev 'grep|tail' | wc -l)

        if [ $wc_main -gt 0 ]
        then
                echo "$dNow $proc_main $wc_main"
                #renice_proc  $proc_sub $ni_low
                renice_proc  $proc_main $ni_high
                renice_proc  $proc_main2 $ni_high
                wait_finish  $proc_main
                #renice_proc  $proc_sub $ni_normal
        else
                echo "$dNow sleeping..."
        fi
        sleep 1
done