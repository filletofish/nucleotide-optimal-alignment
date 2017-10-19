import numpy as np

from Source.needleman_wunsch import needleman_wunsch
from Source.scroring_functions import default_similarity_func


def __fill_matrix(first_chain, second_chain, split_coefficient, gap_penalty = -1, similarity_func = default_similarity_func):
    """

    :param first_chain: np array of letters
    :param second_chain: np array of letters
    :param gap_penalty: penalty for gap insertion
    :param similarity_func: func having 2 chars as params returning score for similarity
    :return: np matrix filled with scores
    """
    matrix = np.zeros((len(first_chain) + 1, len(second_chain) + 1))

    for i in range(split_coefficient):
        matrix[i][0] = gap_penalty * i

    for j in range(split_coefficient):
        matrix[0][j] = gap_penalty * j

    for i in range(0, len(first_chain)):
        for j in range(0, len(second_chain)):
            if j < split_coefficient and i > split_coefficient + j:
                continue

            if i < split_coefficient and j > split_coefficient + i:
                continue

            match = matrix[i][j] + similarity_func(first_chain[i], second_chain[j])
            delete = matrix[i][j + 1] + gap_penalty
            insert = matrix[i + 1][j] + gap_penalty
            matrix[i + 1][j + 1] = max(match, delete, insert)

    return matrix


def __trace_back(first_chain, second_chain, matrix, split_coefficient, gap_penalty = -1,  similarity = default_similarity_func):
    """

    :param first_chain: np array of chars
    :param second_chain: np array of chars
    :param matrix: matrix (n+1, m+1) filled with scores (int)
    :param gap_penalty: penalty for gap insertion
    :param similarity: func having 2 chars as params returning score for similarity
    :return: tuple with two aligned chains (strings)
    """
    alignment_a = ""
    alignment_b = ""
    i = len(first_chain) - 1
    j = len(second_chain) - 1
    while i >= 0 or j >= 0:
        if j < split_coefficient and i > split_coefficient + i:
            i -= 1
            continue

        if i < split_coefficient and j > split_coefficient + j:
            j -= 1
            continue


        if i >= 0 and j >= 0 and matrix[i + 1][j + 1] == matrix[i][j] + similarity(first_chain[i], second_chain[j]):
            alignment_a = first_chain[i] + alignment_a
            alignment_b = second_chain[j] + alignment_b
            i -= 1
            j -= 1
        elif i >= 0 and matrix[i+1][j+1] == matrix[i][j + 1] + gap_penalty:
            alignment_a = first_chain[i] + alignment_a
            alignment_b = "-" + alignment_b
            i -= 1

        else:
            alignment_a = "-" + alignment_a
            alignment_b = second_chain[j] + alignment_b
            j -= 1

    return alignment_a, alignment_b




def optimized_needleman_wunsch(chain_a, chain_b, gap_penalty = -1, similarity_func = default_similarity_func, print_matrix=True):
    split_coefficient = int(max(len(chain_a), len(chain_b)) / 2)
    matrix = __fill_matrix(chain_a, chain_b, split_coefficient, gap_penalty=gap_penalty, similarity_func=similarity_func)
    if print_matrix:
        print(matrix)

    alignments = __trace_back(chain_a, chain_b, split_coefficient=split_coefficient, matrix=matrix, gap_penalty=gap_penalty, similarity=similarity_func)
    return alignments