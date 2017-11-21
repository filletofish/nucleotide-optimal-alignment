from Source.optimized_needleman_wunsch import optimized_needleman_wunsch
from Source.optimized_needleman_wunsch import needleman_wunsch

def wrap_with_gap_penalty(scoring_func, gap_penalty):
    def wrapped(a, b):
        if a == '-' or b == '-':
            return gap_penalty
        if a == '#' or b == '#':
            return 8
        else:
            return scoring_func(a, b)
    return wrapped

def multidimensial_nw(chains, gap_penalty, similarity_func):
    wrapped = wrap_with_gap_penalty(similarity_func, gap_penalty)
    return __multidimensial_nw(chains, gap_penalty, wrapped)

    # return alignments

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def __multidimensial_nw(chains, gap_penalty, similarity_func):
    def mapChainPair(chainPair):
            if len(chainPair) == 2:
                alignments, score = needleman_wunsch(chainPair[0], chainPair[1], similarity_func, gap_penalty, gap_penalty)
                return alignments[0] + '#' + alignments[1]
            elif len(chainPair) == 1:
                return ''.join(chainPair[0]) + '#' + ''.join(chainPair[0])
            else:
                assert False, "Wrong pair of chain size"

    while len(chains) > 1:
        chains_splitted = list(chunks(chains, 2))
        chains = list(map(mapChainPair, chains_splitted))

    print(chains[0])
    return chains[0].split("#")



