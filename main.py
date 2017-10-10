import numpy as np
import time
import sys
from scroring_functions import blosum_62_scoring

def default_similarity_func(a, b):
    return 1 if a == b else -1


def fill_matrix(first_chain, second_chain, gap_penalty = -1, similarity_func = default_similarity_func):
    """

    :param first_chain: np array of letters
    :param second_chain: np array of letters
    :param gap_penalty: penalty for gap insertion
    :param similarity_func: func having 2 chars as params returning score for similarity
    :return: np matrix filled with scores
    """
    matrix = np.zeros((len(first_chain) + 1, len(second_chain) + 1))

    for i in range(len(first_chain) + 1):
        matrix[i][0] = gap_penalty * i

    for j in range(len(second_chain) + 1):
        matrix[0][j] = gap_penalty * j

    for i in range(0, len(first_chain)):
        for j in range(0, len(second_chain)):
            match = matrix[i][j] + similarity_func(first_chain[i], second_chain[j])
            delete = matrix[i][j + 1] + gap_penalty
            insert = matrix[i + 1][j] + gap_penalty
            matrix[i + 1][j + 1] = max(match, delete, insert)

    return matrix


def trace_back(first_chain, second_chain, matrix, gap_penalty = -1,  similarity = default_similarity_func):
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



def main():
    f = open('test_input.txt', 'r')
    str = f.read()
    chain_a_raw, chain_b_raw = str.split("\n")
    chain_a = np.array(list(chain_a_raw))
    chain_b = np.array(list(chain_b_raw))
    matrix = fill_matrix(chain_a, chain_b, gap_penalty=-5, similarity_func=blosum_62_scoring)
    print(matrix)

    aligments = trace_back(chain_a, chain_b, matrix, gap_penalty=-5, similarity=blosum_62_scoring)
    print("Result\n", aligments[0], "\n", aligments[1])
    f.close()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("\nIn %s seconds" % (time.time() - start_time))