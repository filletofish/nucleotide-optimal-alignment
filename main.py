import time

import numpy as np

from Source.scroring_functions import blosum_62_scoring
from Source.smith_waterman import smith_waterman
from Source.hirschberg import hirschberg
from Source.needleman_wunsch import needleman_wunsch
from Source.optimized_needleman_wunsch import optimized_needleman_wunsch


def main():
    f = open('test_input_1.txt', 'r')
    str = f.read()
    chain_a_raw, chain_b_raw = str.split("\n")
    chain_a = np.array(list(chain_a_raw))
    chain_b = np.array(list(chain_b_raw))
    # alignments = needleman_wunsch(chain_a, chain_b, gap_penalty=-5, similarity_func=blosum_62_scoring)
    # alignments = hirschberg(chain_a, chain_b, gap_penalty=-5, similarity_func=blosum_62_scoring)
    #alignments = smith_waterman(chain_a, chain_b, gap_penalty=-5, similarity_func=blosum_62_scoring)

    start_time = time.time()
    alignments = optimized_needleman_wunsch(chain_a, chain_b, gap_penalty=-5, similarity_func=blosum_62_scoring)
    print("\nIn %s seconds" % (time.time() - start_time))
    print("Result\n", alignments[0], "\n", alignments[1])

    start_time = time.time()
    alignments = needleman_wunsch(chain_a, chain_b, gap_penalty=-5, similarity_func=blosum_62_scoring)
    print("\nNot optimizedIn %s seconds" % (time.time() - start_time))
    print("Result\n", alignments[0], "\n", alignments[1])
    f.close()



if __name__ == "__main__":
    start_time = time.time()
    main()
    print("\nIn %s seconds" % (time.time() - start_time))