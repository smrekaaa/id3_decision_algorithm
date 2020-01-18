import pandas as pd
import sys


def read_file(filepath):
    """
    Reads and prints data file
    :param filepath: path to the file
    :return data: pandas dataframe
    :return count: numer of rows in dataframe
    """
    try:
        data = pd.read_csv(filepath, sep=',', encoding='utf8')
        count = len(data.index)
        return data, count
    except FileNotFoundError:
        print("Wrong file or file path.")
        sys.exit(1)


if __name__ == "__main__":

    df_data, r = read_file("./Data/car_ucna.csv")
    print(df_data)
    print("Count: " + str(len(df_data.index)))
    header = df_data.columns

    grouped = df_data.groupby([header[0]])
    print(type(grouped.groups))  # dict
    print(str(grouped.groups['high']))



