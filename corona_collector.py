import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re 
import os
import argparse
from datetime import date
from datetime import datetime

country_global = 1573

def get_virus_spread_info(url, country, file, date_time, verbose) :

	if verbose == 1 :
		print(url)

	virus_response = requests.get(url)
	if verbose == 1 :
		print(virus_response)

	virus_response_soup = BeautifulSoup(virus_response.content, "html.parser")
	#print(virus_response_soup.prettify())

	row_size = 9

	div_class = virus_response_soup.find(class_ = "table")

	row_all = div_class.find_all('td')
	# print(len(row_all))
	
	processed_row_all = []
	url_all = []

	j=0
	temp_row = ""
	country_flag = 0

	for i in range( len(row_all) ) :
		row = row_all[i]
		row_text = row.get_text()
		row_text = row_text.replace('+', '')
		row_text = row_text.replace(',', '')

		if country != "All" and row_text.find(country) != -1 :
			country_flag = 1
			file.write(date_time + ',\t')

		if country_flag == 1 :
			if j%row_size != row_size-1 :
				# print(row_text.replace(' ', ''), end = ',\t')
				# print("if country: " + country + " j: " + str(j))
				file.write(row_text.replace(' ', '') + ',\t')
				if verbose > 1 :
					print(row_text.replace(' ', ''), end = ',\t')
			else : 
				# print(row_text.replace(' ', ''), end = '\n')
				# print("else country: " + country + " j: " + str(j))
				file.write(row_text.replace(' ', '') + "\n")
				if verbose > 1 :
					print(row_text.replace(' ', '') + "\n")
				country_flag = 0
			
		# if country == "All" and j%row_size != row_size-1 :
		# 	#row_text = row_text.replace(' ', ''), end = ',\t'
		# 	# print(row_text.replace(' ', ''), end = ',\t')
		# 	file.write(row_text.replace(' ', '') + ',\t')
		# elif country == "All" and j%row_size == row_size-1 : 
		# 	# print(row_text.replace(' ', ''), end = '\n')
		# 	file.write(row_text.replace(' ', '') + "\n")
		# 	processed_row_all.append(temp_row)

		# file.write(row_text)

		# print("PRINTING IN FILE ... ")
		# for i in range(len(attr_all)) :
		# 	print(concatinated_all[i])
		# 	file.write(concatinated_all[i] + "\n")
		# file.close()

		j+=1

	file.close()

def parse_arguments(url_common):
	# print("Parsing arguments ...")
	parser = argparse.ArgumentParser()

	today = date.today()
	# dd/mm/YYYY
	dt = today.strftime("%d")
	mn = today.strftime("%m")
	yr = today.strftime("%Y")
	# print("dt =", dt)
	# print("mn =", mn)
	# print("yr =", yr)
	current_date = mn + "/" + dt + "/" + yr

	now = datetime.now().strftime("%H:%M:%S")

	date_time = str(current_date) + "  " + str(now)


	parser.add_argument("-c", "--country", type=str, default="USA")
	parser.add_argument("-v", "--verbose", type=int, default=0)
	parser.add_argument("-x", "--counter_arg", type=int, default=0)
	# parser.add_argument("-s", "--start_date", type=str, default=current_date)
	# parser.add_argument("-e", "--end_date", type=str, default=current_date)

	args = parser.parse_args()
	country = args.country
	verbose = args.verbose
	counter_arg = args.counter_arg

	if verbose == 1 :
		print("Parsing complete !!!")

	# 1/5/2020  11:34:00 PM

	if verbose == 1 :
		print("country = ", country)
		print("current_datetime = ", datetime)

	filename = country + "_corona_stats" + ".csv"
	file = open(country + "_corona_stats" + ".csv", "a")
	if counter_arg == 1 and os.stat(filename).st_size == 0 :
		file.write("date_time, country, total_cases, new_cases, total_deaths, new_deaths, total_recs, active_cases, critical_cases, cases_per_M_pop \n")
	url = url_common #+ country
	get_virus_spread_info(url, country, file, date_time, verbose)
	file.close()
			
if __name__ == "__main__":
	# print("In main ...")

	url_common = 'https://www.worldometers.info/coronavirus/'
	
	parse_arguments(url_common)






