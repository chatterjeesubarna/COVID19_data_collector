#!/bin/sh  

absolute_path=$(pwd)
m_absolute_path="$absolute_path/"
result_path="$absolute_path/results" 
#echo $absolute_path

sleep_duration=300
end_after=86400
counter_arg=0
while true  
do  
  now=$(date)
  echo "******** Collecting data for COVID-19 at $now ******* "

  counter_arg=$((counter_arg+1))
  #command="python3 corona_collector.py -x $counter_arg -c USA"
  python3 corona_collector.py -x $counter_arg -c USA -v 2	
  sleep 2

  cd $result_path 
  Rscript plot.R $m_absolute_path
  echo "plotting done! Check results at $result_path"
  cd ..	
  sleep $sleep_duration 
done	
