#!/bin/sh  

sleep_duration=3
end_after=86400
counter_arg=0
while true  
do  
  counter_arg=$((counter_arg+1))
  command="python3 corona_collector.py -x $counter_arg -c USA"
  #echo $command
  python3 corona_collector.py -x $counter_arg -c USA		
  sleep $sleep_duration  
done	