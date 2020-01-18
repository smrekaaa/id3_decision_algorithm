import numpy as np


def entropy(dic_values, T):
    """
    Calucaltes the entropy.
    :param dic_values: dictionary of distinct classes/atributes and the number of their occurances in dataset
    :param T: Total number of rows in chosen dataset
    :return: entropy
    """
    result = 0
    for c in dic_values:
        p = dic_values[c]

        if p is not 0:
            result += ((-p/T)*np.log2(p/T))

    return result




# Test
if __name__ == "__main__":
    e = entropy({"a": 9, "b": 5}, 14)
    print(e)
