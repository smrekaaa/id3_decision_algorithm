import argparse
import File_manipulations as fm
import id3

# READING ARGUMENTS ----------------------------------------------------------------------------------------------------
parser = argparse.ArgumentParser(description="Arguments for ID3 alghoritm.")

parser.add_argument('-t', type=str, default="./Data/breastcancer_ucna.csv", help="Path to learning csv file.",
                    required=False)
parser.add_argument('-T', type=str, default="./Data/breastcancer_testna.csv", help="Path to a testing csv file.",
                    required=False)
parser.add_argument('-m', type=str, default="information gain", help="Type of the tree metrics",
                    choices=['entropy', 'information gain'], required=False)

parser.add_argument('-i', type=str, default="True", choices=['True', 'False'],
                    help="Shew metrics or not", required=False)

try:
    args = parser.parse_args()
    print(args)
except IOError:
    parser.error("Weren't able to read arguments.")

# ACTUAL START ---------------------------------------------------------------------------------------------------------

# 1. Read learning fil
df_data, head, n_rows = fm.read_file(args.t)  # data set as dataframe and number of rows
# print(df_data)

"""
2. get classes from both datasets and compare them
    - If they're different exit program.
    - Else, set dictionary of classes and their indexes and
        create confuision matrix with all 0 values.
"""

# 2. Create main id3 object and grow the decision tree with leaarning dataset
main_id3 = id3.ID3("ID3 TABLE", df_data, head, n_rows, args.m)
# main_id3.print_out()
main_id3.root.print_out()

"""3. Test the tree"""
# Read test file
test_df_data, test_head, test_n_rows = fm.read_file(args.T)  # data set as dataframe and number of rows

# Check if the classes match
if main_id3.check_classes(test_df_data, test_head):

    # Calculate the confusion matrix
    main_id3.calculate_confusion_mtrx()

    # Print out the confusion matrix
    main_id3.print_confusion_mtr()

    # Print out the metrics
    if args.i == "True":
        print()
        main_id3.calculate_metrics()

print("end")










