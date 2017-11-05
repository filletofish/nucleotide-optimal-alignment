import numpy as np
from Source.gap_penalty_strategy import GapPenaltyStrategy

def __fill_matrix(first_chain, second_chain, similarity_func, gap_penalty_strategy):
    """

    :param first_chain: np array of letters
    :param second_chain: np array of letters
    :param gap_penalty_func: penalty for gap insertion
    :param similarity_func: func having 2 chars as params returning score for similarity
    :return: np matrix filled with scores
    """
    matrix = np.zeros((len(first_chain) + 1, len(second_chain) + 1))

    for i in range(len(first_chain) + 1):
        if i == 0:
            matrix[i][0] = 0
        else:
            matrix[i][0] = matrix[i-1][0] - gap_penalty_strategy.get_insert_gap_penalty(i, 0)
            gap_penalty_strategy.record_insert_gap_penalty(i, 0)

    for j in range(len(second_chain) + 1):
        if j == 0:
            matrix[0][j] = 0
        else:
            matrix[0][j]= matrix[0][j-1] - gap_penalty_strategy.get_delete_gap_penalty(0, j)
            gap_penalty_strategy.record_delete_gap_penalty(0, j)

    for i in range(0, len(first_chain)):
        for j in range(0, len(second_chain)):
            match = matrix[i][j] + similarity_func(first_chain[i], second_chain[j])
            delete = matrix[i + 1][j] - gap_penalty_strategy.get_delete_gap_penalty(i+1, j+1)
            insert = matrix[i][j + 1] - gap_penalty_strategy.get_insert_gap_penalty(i+1, j+1)

            matrix[i + 1][j + 1] = max(match, delete, insert)

            if matrix[i+1][j+1] == delete:
                gap_penalty_strategy.record_delete_gap_penalty(i+1, j+1)
            elif matrix[i+1][j+1] == insert:
                gap_penalty_strategy.record_insert_gap_penalty(i+1, j+1)

    return matrix


def __trace_back(first_chain, second_chain, matrix, similarity_func, gap_penalty_strategy):
    """

    :param first_chain: np array of chars
    :param second_chain: np array of chars
    :param matrix: matrix (n+1, m+1) filled with scores (int)
    :param gap_penalty_func: penalty for gap
    :param similarity: func having 2 chars as params returning score for similarity
    :return: tuple with two aligned chains (strings)
    """
    alignment_a = ""
    alignment_b = ""
    i = len(first_chain) - 1
    j = len(second_chain) - 1
    while i >= 0 or j >= 0:
        score_similarity = similarity_func(first_chain[i], second_chain[j])
        score_insert = -gap_penalty_strategy.get_insert_gap_penalty(i+1, j+1)
        score_delete = -gap_penalty_strategy.get_delete_gap_penalty(i+1, j+1)

        if i >= 0 and j >= 0 and matrix[i + 1][j + 1] == matrix[i][j] + score_similarity:
            alignment_a = first_chain[i] + alignment_a
            alignment_b = second_chain[j] + alignment_b
            i -= 1
            j -= 1
        elif i >= 0 and matrix[i+1][j+1] == matrix[i][j + 1] + score_insert:
            alignment_a = first_chain[i] + alignment_a
            alignment_b = "-" + alignment_b
            i -= 1

        elif j >= 0 and matrix[i+1][j+1] == matrix[i+1][j] + score_delete:
            alignment_a = "-" + alignment_a
            alignment_b = second_chain[j] + alignment_b
            j -= 1
        else:
            assert False, "Should not reach this point"


    return alignment_a, alignment_b


def needleman_wunsch(chain_a, chain_b, similarity_func, print_matrix=True):
    gap_penalty_strategy = GapPenaltyStrategy(chain_a, chain_b, 10, 2)
    matrix = __fill_matrix(chain_a, chain_b, similarity_func=similarity_func, gap_penalty_strategy=gap_penalty_strategy)
    if print_matrix:
        print(matrix)

    aligments = __trace_back(chain_a, chain_b, matrix, similarity_func=similarity_func, gap_penalty_strategy=gap_penalty_strategy)
    return aligments