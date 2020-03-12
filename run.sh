#!/bin/sh  

absolute_path=$(PWD)
result_path="$absolute_path/results" 
echo $result_path

sleep_duration=30
end_after=86400
counter_arg=0
while true  
do  
  now=$(date)
  echo "\n******* Collecting data for COVID-19 at $now ******* "

  counter_arg=$((counter_arg+1))
  #command="python3 corona_collector.py -x $counter_arg -c USA"
  python3 corona_collector.py -x $counter_arg -c USA -v 2	
  sleep 2

  cd $result_path 
  ls
  Rscript plot.R
  echo "plotting done! Check results at $result_path"
  cd ..	
  sleep $sleep_duration 
done	