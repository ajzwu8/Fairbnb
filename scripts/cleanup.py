import pandas as pd
import numpy as np
from ast import literal_eval

CSV_FILE = "../listings.csv"    # csv file of data
ROWS_FILE = "rows_to_keep.txt"  # text containing rows to keep


def convert_to_feature(data):
	""" Applies this function to every cell in the csv. Goal is
	    to convert every cell into a numeral.

	    Example conversions include removing deciamals, dollar signs,
	    converting booleans to bits (true -> 1, false -> 0), converting
	    lists into their lengths as a feature. """

	# null things should be 0 (subject to change)
	if pd.isnull(data):
		return 0

	# for strings, try and clean up into an int
	if type(data) == str:
		# special case for lists
		try:
			eval_data = literal_eval(data)
			if type(eval_data) == list:
				return len(eval_data)
		except:
			# turn booleans into bits
			if data == 't':
				return 1
			elif data == 'f':
				return 0
			# turn prices into numbers
			elif '$' in data:
				return float(data[1:].replace(',',''))
			# percents become decimals
			elif '%' in data:
				return float(data.replace('%',''))

	# default, return itself
	return data


def cleanup():
	""" Consumes raw data in order to filter our unecessary columns."""
	cols_to_keep = []
	with open(ROWS_FILE, 'r') as r_file:
		cols_to_keep = r_file.read().split(',')

	assert(len(cols_to_keep))
	data = pd.read_csv(CSV_FILE)
	
	# trim data and apply feature conversion
	trimmed_data = data[cols_to_keep]
	trimmed_data = trimmed_data.applymap(convert_to_feature)
	trimmed_data.to_csv('listings_cleaned.csv', index=False)

if __name__ == '__main__':
	cleanup()
	print "Data cleaned."