import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re 
import argparse
from datetime import date

def get_virus_spread_info(url, country, file) :

	virus_response = requests.get(url)
	print(virus_response)

	virus_response_soup = BeautifulSoup(virus_response.content, "html.parser")
	print(virus_response_soup.prettify())

	row_size = 7

	if virus_response_soup.find(class_ = "notTradingIPO"):
		print("Market closed -- no data available!")
		return

	div_class = virus_response_soup.find(class_ = "DividendCalendar")

	row_all = div_class.find_all('td')
	processed_row_all = []
	url_all = []

	j=0
	temp_row = ""

	for i in range( len(row_all) ) :
		row = row_all[i]
		row_text = row.get_text()
		if j%row_size != row_size-1 :
			# print(row_text.replace(',', ''), end = ',\t')
			# file.write(row_text.replace(',', '') + " , ")
			temp_row = temp_row + row_text.replace(',', '') + " , "
		else: 
			# print(row_text.replace(',', ''), end = '\n')
			# file.write(row_text.replace(',', '') + "\n")
			temp_row = temp_row + row_text.replace(',', '') 
			processed_row_all.append(temp_row)
			temp_row = ""

		# convert nasdaq url to new.nasdaq url
		if row.find('a') :
			row_url = row.a['href'].replace('/dividend-history', '')
			# url_all.append(row_url.replace('www.nasdaq.com/symbol', 'new.nasdaq.com/market-activity/stocks'))
			url_all.append(row_url)

		j+=1

	get_stock_info(url_all, processed_row_all, file)

def get_stock_info(url_all, processed_row_all, file) :

	attr_all = []
	for i in range( len(url_all) ) : # range(1) : #
		temp_attr = ""

		new_nasdaq_stock_url = url_all[i]
		print("Fetching", url_all[i])

		new_nasdaq_stock_response = requests.get(new_nasdaq_stock_url)
		print(new_nasdaq_stock_response)

		new_nasdaq_stock_soup = BeautifulSoup(new_nasdaq_stock_response.content, "html.parser")

		stock_class = new_nasdaq_stock_soup.find(class_ = "row overview-results relativeP")

		cell_all = stock_class.find_all(class_ = "table-cell")

		attr_counter = 0
		for i in range( len(cell_all) ):
			temp_key = cell_all[i].get_text()
			if "1 Year" in temp_key :
				attr_counter = 1
				i+=1
				temp_val = cell_all[i].get_text().strip()
				if "." not in temp_val and "1" not in temp_val and "2" not in temp_val and "3" not in temp_val and "4" not in temp_val and "5" not in temp_val and "6" not in temp_val and "7" not in temp_val and "8" not in temp_val and "9" not in temp_val:
					temp_attr = temp_attr + "-, "
				else :
					temp_attr = temp_attr + temp_val.strip() + ", "
				
				print("attr_counter = ", attr_counter)
				print(temp_attr.strip())

			elif "Today" in temp_key :
				if attr_counter != 1 :
					while attr_counter != 1 :
						temp_attr = temp_attr + "-, "
						attr_counter+=1
				
				attr_counter+=1
				i+=1
				temp_val = cell_all[i].get_text().strip()
				if "$" not in temp_val :
					temp_attr = temp_attr + "-, "
				else :
					temp_val = temp_val.replace("\xa0", '')
					temp_val = temp_val.replace("$", '')
					result = re.split('/', temp_val)
					avg = ( float(result[0]) + float(result[1]) ) / 2
					# print(avg)
					temp_attr = temp_attr + str(round(avg, 2)) + ", "

				print("attr_counter = ", attr_counter)
				for i in range(len(temp_attr)):
					print(temp_attr[i], end = "")

			elif "Share Volume" in temp_key :
				if attr_counter != 2 :
					while attr_counter != 2 :
						temp_attr = temp_attr + "-, "
						attr_counter+=1
				
				attr_counter+=1
				i+=1
				temp_val = cell_all[i].get_text().strip()
				if "," not in temp_val :
					temp_attr = temp_attr + "-, "
				else :
					temp_val = temp_val.replace("\xa0", '')
					temp_val = temp_val.replace(",", '')
					temp_attr = temp_attr + temp_val.strip() + ", "

				print("\n attr_counter = ", attr_counter)
				for i in range(len(temp_attr)):
					print(temp_attr[i], end = "")

			elif "52 Week" in temp_key :
				if attr_counter != 3 :
					while attr_counter != 3 :
						temp_attr = temp_attr + "-, "
						attr_counter+=1
				
				attr_counter+=1
				i+=1
				temp_val = cell_all[i].get_text().strip()
				if "$" not in temp_val :
					temp_attr = temp_attr + "-, "
				else :
					temp_val = temp_val.replace("\xa0", '')
					temp_val = temp_val.replace("$", '')
					result = re.split('/', temp_val)
					growth_percentage = ( float(result[0]) - float(result[1]) ) * 100 / float(result[1])
					# print(growth_percentage)
					temp_attr = temp_attr + str(round(growth_percentage, 2)) + ", "

				print("\n attr_counter = ", attr_counter)
				for i in range(len(temp_attr)):
					print(temp_attr[i], end = "")

			elif "Market Cap" in temp_key :
				if attr_counter != 4 :
					while attr_counter != 4 :
						temp_attr = temp_attr + "-, "
						attr_counter+=1
				
				attr_counter+=1
				i+=1
				temp_val = cell_all[i].get_text().strip()
				if "," not in temp_val :
					temp_attr = temp_attr + "-, "
				else :
					temp_val = temp_val.replace("\xa0", '')
					temp_val = temp_val.replace(",", '')
					temp_attr = temp_attr + temp_val.strip() + ", "

				print("\n attr_counter = ", attr_counter)
				for i in range(len(temp_attr)):
					print(temp_attr[i], end = "")

			elif "P/E Ratio" in temp_key :
				if attr_counter != 5 :
					while attr_counter != 5 :
						temp_attr = temp_attr + "-, "
						attr_counter+=1
				
				attr_counter+=1
				i+=1
				temp_val = cell_all[i].get_text().strip()
				if "." not in temp_val and "1" not in temp_val and "2" not in temp_val and "3" not in temp_val and "4" not in temp_val and "5" not in temp_val and "6" not in temp_val and "7" not in temp_val and "8" not in temp_val and "9" not in temp_val:
					temp_attr = temp_attr + "-, "
				else :
					temp_val = temp_val.replace("\xa0", '')
					temp_attr = temp_attr + temp_val.strip() + ", "

				print("\n attr_counter = ", attr_counter)
				for i in range(len(temp_attr)):
					print(temp_attr[i], end = "")

			elif "Forward P/E" in temp_key :
				if attr_counter != 6 :
					while attr_counter != 6 :
						temp_attr = temp_attr + "-, "
						attr_counter+=1
				
				attr_counter+=1
				i+=1
				temp_val = cell_all[i].get_text().strip()
				if "." not in temp_val and "1" not in temp_val and "2" not in temp_val and "3" not in temp_val and "4" not in temp_val and "5" not in temp_val and "6" not in temp_val and "7" not in temp_val and "8" not in temp_val and "9" not in temp_val:
					temp_attr = temp_attr + "-, "
				else :
					temp_val = temp_val.replace("\xa0", '')
					temp_attr = temp_attr + temp_val.strip() + ", "

				print("\n attr_counter = ", attr_counter)
				for i in range(len(temp_attr)):
					print(temp_attr[i], end = "")

			elif "EPS" in temp_key :
				if attr_counter != 7 :
					while attr_counter != 7 :
						temp_attr = temp_attr + "-, "
						attr_counter+=1
				
				attr_counter+=1
				i+=1
				temp_val = cell_all[i].get_text().strip()
				if "$" not in temp_val :
					temp_attr = temp_attr + "-, "
				else :
					temp_val = temp_val.replace("\xa0", '')
					temp_val = temp_val.replace("$", '')
					temp_attr = temp_attr + temp_val.strip() + ", "

				print("\n attr_counter = ", attr_counter)
				for i in range(len(temp_attr)):
					print(temp_attr[i], end = "")

			elif "Yield" in temp_key :
				print("\n IN HERE:: attr_counter = ", attr_counter)
				if attr_counter != 8 :
					while attr_counter != 8 :
						temp_attr = temp_attr + "-, "
						attr_counter+=1
				
				attr_counter+=1
				i+=1
				print("\n NOW HERE:: attr_counter = ", attr_counter)
				temp_val = cell_all[i].get_text().strip()
				if "%" not in temp_val :
					temp_attr = temp_attr + "-"
				else :
					temp_val = temp_val.replace("\xa0", '')
					temp_val = temp_val.replace("%", '')
					temp_attr = temp_attr + temp_val.strip() 

				print("\n attr_counter = ", attr_counter)
				for i in range(len(temp_attr)):
					print(temp_attr[i], end = "")

		while attr_counter != 9 :
			temp_attr = temp_attr + "-, "
			attr_counter+=1

		print("\n attr_counter = ", attr_counter)
		print("DONE")
		for i in range(len(temp_attr)):
			print(temp_attr[i], end = "")
		print("\n")

		attr_all.append(temp_attr)

	concatinated_all = []
	for i in range(len(attr_all)) :
		print(attr_all[i])
		concatinated_all.append( str(processed_row_all[i]) + ", " + str(attr_all[i]) )

	print("PRINTING IN FILE ... ")
	for i in range(len(attr_all)) :
		print(concatinated_all[i])
		file.write(concatinated_all[i] + "\n")
	file.close()

def parse_arguments(url_common):
	print("Parsing arguments ...")
	parser = argparse.ArgumentParser()

	today = date.today()
	# dd/mm/YY
	dt = today.strftime("%d")
	mon = today.strftime("%b")
	mn = today.strftime("%m")
	yr = today.strftime("%Y")
	# print("dt =", dt)
	# print("mon =", mon)
	# print("mn =", mn)
	# print("yr =", yr)
	current_date = yr + "-" + mon + "-" + dt

	parser.add_argument("-c", "--country", type=str, default="usa")
	# parser.add_argument("-s", "--start_date", type=str, default=current_date)
	# parser.add_argument("-e", "--end_date", type=str, default=current_date)

	args = parser.parse_args()
	country = args.country
	# start_date = args.start_date
	# end_date = args.end_date

	print("Parsing complete !!!")

	# url_start = url_common + start_date
	# url_end = url_common + end_date
	print("country =", country)

	file = open(country + "corona_stats" + ".csv", "w+")
	file.write("date_time, country, new_cases \n")
	file.close()
	url = url_common + country
	get_virus_spread_info(url, country, file)

			
if __name__ == "__main__":
	print("In main ...")

	url_common = 'https://www.worldometers.info/coronavirus/country/us/'
	
	parse_arguments(url_common)






