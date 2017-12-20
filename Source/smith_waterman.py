import numpy as np

from Source.scroring_functions import default_similarity_func


def __fill_matrix(first_chain, second_chain, gap_penalty = -1, similarity_func = default_similarity_func):
    """

    :param first_chain: np array of letters
    :param second_chain: np array of letters
    :param gap_penalty: penalty for gap insertion
    :param similarity_func: func having 2 chars as params returning score for similarity
    :return: np matrix filled with scores
    """
    matrix = np.zeros((len(first_chain) + 1, len(second_chain) + 1))

    for i in range(0, len(first_chain)):
        for j in range(0, len(second_chain)):
            match = matrix[i][j] + similarity_func(first_chain[i], second_chain[j])
            delete = matrix[i + 1][j] - gap_penalty
            insert = matrix[i][j + 1] - gap_penalty
            matrix[i + 1][j + 1] = max(match, delete, insert, 0)

    return matrix


def __maximum_score(matrix):
    n, m = matrix.shape

    max_val = 0
    max_val_i = n - 1
    max_val_j = m - 1

    for i in range(n-1, 0, -1):
        for j in range(m-1, 0, -1):
            if matrix[i][j] > max_val:
                max_val = matrix[i][j]
                max_val_i = i
                max_val_j = j

    return max_val, max_val_i, max_val_j

def __trace_back(first_chain, second_chain, matrix, gap_penalty = -1,  similarity = default_similarity_func):
    """

    :param first_chain: np array of chars
    :param second_chain: np array of chars
    :param matrix: matrix (n+1, m+1) filled with scores (int)
    :param gap_penalty: penalty for gap insertion
    :param similarity: func having 2 chars as params returning score for similarity
    :return: tuple with two aligned chains (strings)
    """

    max_val, max_val_i, max_val_j = __maximum_score(matrix)

    alignment_a = ""
    alignment_b = ""
    i = max_val_i
    j = max_val_j
    value = max_val
    while (i > 0 or j > 0) and value != 0:
        if i > 0 and j > 0 and matrix[i][j] == matrix[i-1][j-1] + similarity(first_chain[i - 1], second_chain[j - 1]):
            alignment_a = first_chain[i - 1] + alignment_a
            alignment_b = second_chain[j - 1] + alignment_b
            i -= 1
            j -= 1
        elif i > 0 and matrix[i][j] == matrix[i - 1][j] + gap_penalty:
            alignment_a = first_chain[i - 1] + alignment_a
            alignment_b = "-" + alignment_b
            i -= 1

        else:
            alignment_a = "-" + alignment_a
            alignment_b = second_chain[j - 1] + alignment_b
            j -= 1

        value = matrix[i][j]

    return alignment_a, alignment_b


# TGTTACGG
# GGTTGACTA
#
# Result:
# G T T - A C
# G T T G A C

def smith_waterman(chain_a, chain_b, gap_penalty = 1, similarity_func = default_similarity_func, print_matrix=False):
    matrix = __fill_matrix(chain_a, chain_b, gap_penalty=gap_penalty, similarity_func=similarity_func)
    alignments = __trace_back(chain_a, chain_b, matrix, gap_penalty=gap_penalty, similarity=similarity_func)
    score = matrix[-1][-1]
    return alignments, score