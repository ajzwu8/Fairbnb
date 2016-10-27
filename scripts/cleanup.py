import pandas as pd

CSV_FILE = "../listings.csv"    # csv file of data
ROWS_FILE = "rows_to_keep.txt"  # text containing rows to keep

def cleanup():
	cols_to_keep = []
	with open(ROWS_FILE, 'r') as r_file:
		cols_to_keep = r_file.read().split(',')

	assert(len(cols_to_keep))
	data = pd.read_csv(CSV_FILE)
	
	trimmed_data = data[cols_to_keep]
	trimmed_data.to_csv('listings_cleaned.csv', index=False)

if __name__ == '__main__':
	cleanup()
	print "Data cleaned."