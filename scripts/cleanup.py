import pandas as pd
import numpy as np
from datetime import datetime
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

	# special case for lists
	try:
		eval_data = literal_eval(data)
		if type(eval_data) == list:
			return len(eval_data)
	except:
		pass

	# special case for dates
	try:
		date_data = datetime.strptime(data, '%Y-%m-%d')
		now = datetime.now()
		return (now.year - date_data.year) * 12 + (now.month - date_data.month)
	except:
		pass

	# for strings, try and clean up into an int
	if type(data) == str:
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
			return float(data.replace('%',''))/100.0
		# amenities are a set in this {format}, # amenities = # commas + 1
		elif '{' in data and '}' in data:
			return data.count(',') + 1
		
	# default, return itself
	return data


def one_hot_encoding(df, feature_columns):
	""" Take the pandas dataframe df and create a one-hot encoding for
		each of the feature_columns, then drop the actual feature_column
		as we don't need it anymore. """
	for col in feature_columns:
		one_hot = pd.get_dummies(df[col])
		one_hot.rename(columns = lambda c: "%s_%s" % (col, c.replace(' ','_').lower()), inplace = True)
		df.drop(col, axis = 1, inplace = True)
		df =  df.join(one_hot)

	return df

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
	trimmed_data = one_hot_encoding(trimmed_data, ['property_type', 'room_type', 'bed_type', 'cancellation_policy'])
	trimmed_data.to_csv('listings_cleaned.csv', index=False)

if __name__ == '__main__':
	cleanup()
	print "Data cleaned."