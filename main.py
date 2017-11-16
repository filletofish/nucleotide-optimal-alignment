import time
import argparse

from Source.scroring_functions import blosum_62_scoring
from Source.smith_waterman import smith_waterman
from Source.hirschberg import hirschberg
from Source.needleman_wunsch import needleman_wunsch
from Source.optimized_needleman_wunsch import optimized_needleman_wunsch
from Source.input_output import read_input
from Source.input_output import print_output


def main(filename, algorithm_type, gap_penalty_open, gap_penalty_extension):
    assert algorithm_type == 'nw', 'Choosing other algs is not supported now'

    with open(filename, 'r') as content_file:
        content = content_file.read()
        chains = read_input(content)
        alignments, score = needleman_wunsch(chains[0].chain, chains[1].chain,
                                             similarity_func=blosum_62_scoring,
                                             gap_initial=gap_penalty_open,
                                             gap_cont=gap_penalty_extension)
        print_output(chains[0].name, chains[1].name, alignments[0], alignments[1], score)

    # alignments, score = needleman_wunsch(chain_a, chain_b, gap_penalty=-5, similarity_func=blosum_62_scoring)
    # alignments = hirschberg(chain_a, chain_b, gap_penalty=-5, similarity_func=blosum_62_scoring)
    # alignments, score = smith_waterman(chain_a, chain_b, gap_penalty=-5, similarity_func=blosum_62_scoring)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
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