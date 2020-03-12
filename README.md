# COVID19_data_collector

This repository is intended for real-time collection of data concerning COVID-19. The idea is to provide a simple framework that facilitates customized analytics on the data so that we can derive and spread more awareness about the situation.

To use the repository simply you need to install python3. Then, clone the repository and run the following:

cd COVID19_data_collector
make

This will run the data collection program that collects data for each country (right now, it is only for USA, but you can change it inside run.sh) after every 30 seconds (also modifiable) until you terminate. 

You can check the results inside COVID19_data_collector/results.