import time

import numpy as np

from Source.scroring_functions import blosum_62_scoring
from Source.smith_waterman import smith_waterman


def main():
    f = open('test_input_1.txt', 'r')
    str = f.read()
    chain_a_raw, chain_b_raw = str.split("\n")
    chain_a = np.array(list(chain_a_raw))
    chain_b = np.array(list(chain_b_raw))

    alignments = smith_waterman(chain_a, chain_b, gap_penalty=-5, similarity_func=blosum_62_scoring)
    print("Result\n", alignments[0], "\n", alignments[1])
    f.close()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("\nIn %s seconds" % (time.time() - start_time))