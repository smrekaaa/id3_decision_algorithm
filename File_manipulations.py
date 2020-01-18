import pandas as pd
import sys


def read_file(filepath):
    """
    Reads and prints data file
    :param filepath: path to the file
    :return data: pandas dataframe
    """
    try:
        data = pd.read_csv(filepath, sep=',', encoding='utf8')
        return data
    except FileNotFoundError:
        print("Wrong file or file path.")
        sys.exit(1)




"""
    data_dic = data.to_dict()

    razreda = data.razred.unique()

    print(razreda[0])
"""
