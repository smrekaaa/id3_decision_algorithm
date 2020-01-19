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
        data = pd.read_csv(filepath, sep=',', encoding='utf8')      # Dataframe of csv file
        header = list(data.columns.values.tolist())                 # Header of csv file
        count = len(data.index)                                     # Number of data rows
        return data, header, count
    except FileNotFoundError:
        print("Wrong file or file path.")
        sys.exit(1)


if __name__ == "__main__":

    df_data, header, r = read_file("./Data/car_ucna.csv")
    print(df_data)
    print("Count: " + str(len(df_data.index)))
    print("Header: " + str(header))
    print("Header type: " + str(type(header)))
    print(header[0])
    """grouped = df_data.groupby([header[0]])
    print(type(grouped.groups))  # dict
    print(str(grouped.groups['high']))"""



