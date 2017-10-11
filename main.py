import numpy as np
import time
import sys
from scroring_functions import blosum_62_scoring
from needleman_wunsch import needleman_wunsch
from hirschberg import hirschberg


def main():
    f = open('test_input.txt', 'r')
    str = f.read()
    chain_a_raw, chain_b_raw = str.split("\n")
    chain_a = np.array(list(chain_a_raw))
    chain_b = np.array(list(chain_b_raw))

    alignments = hirschberg(chain_a, chain_b, gap_penalty=-5, similarity_func=blosum_62_scoring)
    print("Result\n", alignments[0], "\n", alignments[1])
    f.close()


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("\nIn %s seconds" % (time.time() - start_time))