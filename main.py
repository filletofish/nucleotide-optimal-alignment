import time
import argparse

from Source.scroring_functions import blosum_62_scoring
from Source.smith_waterman import smith_waterman
from Source.hirschberg import hirschberg
from Source.needleman_wunsch import needleman_wunsch
from Source.optimized_needleman_wunsch import optimized_needleman_wunsch
from Source.multidimensial_nw import multidimensial_nw

import Source.input_output as io


def main(filename, algorithm_type, gap_penalty_open, gap_penalty_extension):
    with open(filename, 'r') as content_file:
        content = content_file.read()
        chains = io.read_input(content)

        if algorithm_type == 'nw':

            alignments, score = needleman_wunsch(chains[0].chain, chains[1].chain,
                                             similarity_func=blosum_62_scoring,
                                             gap_initial=gap_penalty_open,
                                             gap_cont=gap_penalty_extension)
            io.print_output(chains[0].name, chains[1].name, alignments[0], alignments[1], score)

        elif algorithm_type == 'onw':
            alignments, score = optimized_needleman_wunsch(chains[0].chain,
                                                           chains[1].chain,
                                                           gap_penalty=gap_penalty_extension,
                                                           similarity_func=blosum_62_scoring)
            io.print_output(chains[0].name, chains[1].name, alignments[0], alignments[1], score)

        elif algorithm_type == 'sw':
            alignments, score = smith_waterman(chains[0].chain,
                                               chains[1].chain,
                                               gap_penalty=gap_penalty_extension,
                                               similarity_func=blosum_62_scoring)
            io.print_output(chains[0].name, chains[1].name, alignments[0], alignments[1], score)

        elif algorithm_type == 'hb':
            alignments = hirschberg(chains[0].chain,
                                           chains[1].chain,
                                           gap_penalty=gap_penalty_extension,
                                           similarity_func=blosum_62_scoring)
            io.print_output(chains[0].name, chains[1].name, alignments[0], alignments[1], None)

        elif algorithm_type == 'mnw':
            chains_raw = [c.chain for c in chains]
            alignments = multidimensial_nw(chains_raw, gap_penalty_extension, blosum_62_scoring)
            chains_str = ["".join(c) for c in chains_raw]
            io.print_output_multi(chains_str, alignments)

        else:
            assert False, 'Wrong algorythm type'


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

    parser.add_argument('algorithm', choices=['nw', 'onw', 'sw', 'hb', 'mnw'],
                        help='Choose which algorithm to use: nw - Needleman-Wunsch, onw - Optimized Needleman-Wunsch,'
                             'sw - Smith-Waterman, hb - Hirschberg.')

    args = parser.parse_args()
    filename = args.input[0].name
    algorithm_type = args.algorithm
    gap_penalty_open = args.ogap
    gap_penalty_extension = args.egap

    main(filename, algorithm_type, gap_penalty_open, gap_penalty_extension)