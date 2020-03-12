#!/bin/sh  

sleep_duration=3
end_after=86400
while true  
do  
  echo "hello"	
  python3 corona_collector.py
  sleep $sleep_duration  
done	