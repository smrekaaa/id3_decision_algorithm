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


def accuracy(matrix):
    """
    Calculates the accuracy of the matrix
    :param matrix: confusion matrix
    :return: accuracy
    """
    tp = np.trace(matrix)
    t = np.sum(matrix)
    return tp / t


def precisions(matrix):
    """
    Calculates the precisions of each class
    :param matrix: confusion matrix
    :return: array of precisions
    """
    precs = []
    for i in range(len(matrix)):

        tp = matrix[i][i]
        tpfp = np.sum(matrix, axis=0)[i]

        prec = tp / (tpfp)
        precs.append(prec)

    return precs


def precision(precs):
    """
    Calculates average precision
    :param precs: array of precisions
    :return: avg
    """
    return np.average(precs)


def recalls(matrix):
    """
    Calculates the recall of classes
    :param matrix: confusion matrix
    :return: array of recalls
    """
    recs = []

    for i in range(len(matrix)):
        tp = matrix[i][i]
        fntp = np.sum(matrix, axis=1)[i]

        rec = tp / (fntp)
        recs.append(rec)

    return recs


def recall(recs):
    """
    Calculates average recall
    :param recs: all the recalls
    :return: avg
    """
    return np.average(recs)


def class_f_scores(matrix, recs, precs):
    """
    Calcultes f-scores for each class
    :param matrix: confusion martrix
    :param recs: array of recall values
    :param precs: array of precision values
    :return: array of f-scores
    """

    f_scores = []
    for i in range(len(matrix)):
        fsc = 2*((recs[i]*precs[i])/(recs[i]+precs[i]))
        f_scores.append(fsc)

    return f_scores


def f_score(matrix, f_scores):
    """
    Calculates the f-score of the whole matrix
    :param matrix: confusion matrix
    :param f_scores: list of f-scores
    :return: f score
    """
    t = np.sum(matrix)
    f = 0
    for i in range(len(matrix)):
        f += ((np.sum(matrix, axis=1)[i])/t)*f_scores[i]

    return f


# Test
if __name__ == "__main__":
    e = entropy({"a": 9, "b": 5}, 14)
    print(e)

    mtr = [[18, 7, 0],
           [2, 22, 1],
           [0, 21, 29]]

    print(accuracy(mtr))
    precs = precisions(mtr)
    print(precs)
    recs = recalls(mtr)
    print(recs)
    f_scores = class_f_scores(mtr, recs, precs)
    print(f_scores)
    print(f_score(mtr, f_scores))
