import pandas as pd
import numpy as np

CSV_FILE = 'listings_cleaned.csv'
TRAIN_FILE = 'listings_cleaned_train.csv'
TEST_FILE = 'listings_cleaned_test.csv'
TEST_PERCENT = 20

def split():
    data = pd.read_csv(CSV_FILE)
    msk = np.random.rand(len(data)) < 0.8
    train = data[msk]
    test = data[~msk]

    train.to_csv(TRAIN_FILE, index=False)
    test.to_csv(TEST_FILE, index=False)

if __name__ == "__main__":
    split()
    print 'Done splitting. Test file located at ' + CSV_FILE
