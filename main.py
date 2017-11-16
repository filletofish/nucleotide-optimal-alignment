import time

import numpy as np
import argparse

from Source.scroring_functions import blosum_62_scoring
from Source.smith_waterman import smith_waterman
from Source.hirschberg import hirschberg
from Source.needleman_wunsch import needleman_wunsch
from Source.optimized_needleman_wunsch import optimized_needleman_wunsch


    f = open('test_input_1.txt', 'r')
    str = f.read()
    chain_a_raw, chain_b_raw = str.split("\n")
    chain_a = np.array(list(chain_a_raw))
    chain_b = np.array(list(chain_b_raw))
    # alignments = needleman_wunsch(chain_a, chain_b, gap_penalty=-5, similarity_func=blosum_62_scoring)
    # alignments = hirschberg(chain_a, chain_b, gap_penalty=-5, similarity_func=blosum_62_scoring)
    # alignments = smith_waterman(chain_a, chain_b, gap_penalty=-5, similarity_func=blosum_62_scoring)
def main(filename, algorithm_type, gap_penalty_open, gap_penalty_extension):

    start_time = time.time()
    alignments = needleman_wunsch(chain_a, chain_b, similarity_func=blosum_62_scoring)
    print("\nNot optimizedIn %s seconds" % (time.time() - start_time))
    print("Result\n", alignments[0], "\n", alignments[1])
    f.close()



if __name__ == "__main__":
    start_time = time.time()
    main()
    print("\nIn %s seconds" % (time.time() - start_time))    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=argparse.FileType(),
                        help='File containing 2 sequences in FASTA format',
                        nargs=1)

    parser.add_argument('-ogap',
                        type=int,
                        default=10,
                        help='Opening gap penalty penalty value for affine gap system')

    parser.add_argument('-egap',
                        type=int,
                        default=2,
                        help='Extension gap penalty value for affine gap system')

    parser.add_argument('algorithm', choices=['nw', 'onw', 'sw', 'hb'],
                        help='Choose which algorithm to use: nw - Needleman-Wunsch, onw - Optimized Needleman-Wunsch,'
                             'sw - Smith-Waterman, hb - Hirschberg.')

    args = parser.parse_args()
    filename = args.input[0].name
    algorithm_type = args.algorithm
    gap_penalty_open = args.ogap
    gap_penalty_extension = args.egap
    print(filename, algorithm_type, gap_penalty_extension, gap_penalty_open)

    main(filename, algorithm_type, gap_penalty_open, gap_penalty_extension)