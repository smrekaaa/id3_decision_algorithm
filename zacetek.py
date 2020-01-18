import argparse
import File_manipulations as fm

# READING ARGUMENTS ----------------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser(description="Arguments for ID3 alghoritm.")

parser.add_argument('-t', type=str, default="breastcancer_ucna.csv", help="Path to learning csv file.", required=False)
parser.add_argument('-T', type=str, default="breastcancer_testna.csv", help="Path to a testing csv file.", required=False)
parser.add_argument('-m', type=str, default="entropy", help="Type of the tree metrics",
                    choices=['entropy', 'information gain'], required=False)

try:
    args = parser.parse_args()
    print(args)
except IOError:
    parser.error("Weren't able to read arguments.")


# FILES ----------------------------------------------------------------------------------------------------------------


df_data = fm.read_file(args.t)  # dataframe od data




