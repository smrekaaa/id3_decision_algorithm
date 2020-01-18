import argparse
import File_manipulations as fm
import id3

# READING ARGUMENTS ----------------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description="Arguments for ID3 alghoritm.")

parser.add_argument('-t', type=str, default="./Data/breastcancer_ucna.csv", help="Path to learning csv file.",
                    required=False)
parser.add_argument('-T', type=str, default="./Data/breastcancer_testna.csv", help="Path to a testing csv file.",
                    required=False)
parser.add_argument('-m', type=str, default="entropy", help="Type of the tree metrics",
                    choices=['entropy', 'information gain'], required=False)

try:
    args = parser.parse_args()
    print(args)
except IOError:
    parser.error("Weren't able to read arguments.")

# ACTUAL START ---------------------------------------------------------------------------------------------------------

# 1. Read the data
df_data, nrows = fm.read_file(args.t)  # data set as dataframe and number of rows
# print(df_data)

# 2. Create main id3 object and set initial values
main_id3 = id3.ID3("ID3 TABLE", df_data, nrows, args.m)
print(main_id3.print_out())

"""
3. Calculate entropies for each attribute/coulmn(-last)
    
    1. For each column except last, classification one:
        1.1 Create new object for the attribute.
        1.2 Set initial values of the object: T, distinct values and the number of their occurrances
        1.1 Group by distinct values in the column -> new table with 'distinct value' and 'class' value
        
"""










