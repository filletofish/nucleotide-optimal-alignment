import numpy as np

from Source.needleman_wunsch import needleman_wunsch


def __nw_score_last_line(first_chain, second_chain, gap_penalty, similarity_func):
    """
    Returns last row of matrix filled by Needleman-Wunsch algorythm. As we need only one last row optimization
    takes place of using not o(n*m) memory but only 2 rows o(min { n, m }).
    :param first_chain:
    :param second_chain:
    :param gap_penalty:
    :param similarity_func:
    :return:
    """
    len_first_chain = len(first_chain)
    len_second_chain = len(second_chain)
    previous_row = np.zeros(shape=(len_second_chain + 1), dtype=np.int)
    current_row = np.zeros(shape=(len_second_chain + 1), dtype=np.int)

    for j in range(1, len_second_chain + 1):
        previous_row[j] = previous_row[j - 1] + gap_penalty

    for i in range(1, len_first_chain + 1):
        current_row[0] = gap_penalty + previous_row[0]
        for j in range(1, len_second_chain + 1):
            score_sub = previous_row[j - 1] + similarity_func(first_chain[i - 1], second_chain[j - 1])
            score_del = previous_row[j] + gap_penalty
            score_ins = current_row[j - 1] + gap_penalty
            current_row[j] = max(score_sub, score_del, score_ins)

        previous_row = current_row
        current_row = [0] * (len_second_chain + 1)

    return previous_row


def __hirschberg(first_chain, second_chain, gap_penalty, similarity_func):
    """
    Recursively divides first chain until small chains where finding best alignment is trivial.
    Uses __nw_score_last_line to find the score of both last lines from left and right. In other words to find
    the point of best alignment path on matrix on given row.

    Uses needleman_wunsch algorithm for matrix with shape 1.

    :param first_chain:
    :param second_chain:
    :param gap_penalty:
    :param similarity_func:
    :return:
    """

    first_aligned, second_aligned = [], []
    length_first_chain, length_second_chain = len(first_chain), len(second_chain)

    if length_first_chain == 0:
        for i in range(length_second_chain):
            first_aligned.append("-" * len(second_chain[i]))
            second_aligned.append(second_chain[i])
    elif length_second_chain == 0:
        for i in range(length_first_chain):
            first_aligned.append(first_chain[i])
            second_aligned.append("-" * len(first_chain[i]))

    elif length_first_chain == 1 or length_second_chain == 1:
        first_aligned, second_aligned = needleman_wunsch(first_chain, second_chain,
                                                         gap_penalty=gap_penalty,
                                                         similarity_func=similarity_func)

    else:

        # Divide and Conquer

        middle_first_chain = int(length_first_chain / 2)

        row_left = __nw_score_last_line(first_chain[:middle_first_chain], second_chain, gap_penalty, similarity_func)
        row_right = __nw_score_last_line(first_chain[middle_first_chain:][::-1], second_chain[::-1], gap_penalty,
                                         similarity_func)

        reversed_row_right = row_right[::-1]

        # Getting maximum
        row = [l + r for l, r in zip(row_left, reversed_row_right)]
        maxidx, maxval = max(enumerate(row), key=lambda a: a[1])

        middle_second_chain = maxidx

        # Recursive calls

        aligned_first_left, aligned_second_left = __hirschberg(first_chain[:middle_first_chain],
                                                               second_chain[:middle_second_chain], gap_penalty,
                                                               similarity_func)
        algined_first_right, aligned_second_right = __hirschberg(first_chain[middle_first_chain:],
                                                                 second_chain[middle_second_chain:], gap_penalty,
                                                                 similarity_func)

        first_aligned = list(aligned_first_left) + list(algined_first_right)
        second_aligned = list(aligned_second_left) + list(aligned_second_right)

    return "".join(first_aligned), "".join(second_aligned)


def hirschberg(first_chain, second_chain, gap_penalty, similarity_func):
    return __hirschberg(first_chain, second_chain, gap_penalty, similarity_func)
