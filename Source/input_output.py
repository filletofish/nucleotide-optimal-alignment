import numpy as np
from Bio import SeqIO
from io import StringIO
from Source.NucleotideChain import NucleotideChain


min_line_length = 20


def read_input(data):
    records = SeqIO.parse(StringIO(data), "fasta")
    return [NucleotideChain(record.id, np.array(record.seq)) for record in records]


def print_output(name_chain_a, name_chain_b, aligned_chain_seq_a, aligned_chain_seq_b, score):
    while len(name_chain_a) > min_line_length and len(name_chain_b) > min_line_length:
        print("1: " + name_chain_a[:min_line_length])
        print("2: " + name_chain_b[:min_line_length])

        name_chain_a = name_chain_a[min_line_length:]
        name_chain_b = name_chain_b[min_line_length:]
    print("1: " + name_chain_a)
    print("2: " + name_chain_b)

    print("\nAligned:\n")

    while len(aligned_chain_seq_a) > min_line_length and len(aligned_chain_seq_b) > min_line_length:
        print("1: " + aligned_chain_seq_a[:min_line_length])
        print("2: " + aligned_chain_seq_b[:min_line_length])
        aligned_chain_seq_a = aligned_chain_seq_a[min_line_length:]
        aligned_chain_seq_b = aligned_chain_seq_b[min_line_length:]
        print("")
    print("1: " + aligned_chain_seq_a)
    print("2: " + aligned_chain_seq_b)

    if score is not None:
        print("\nScore: ", score)


def print_output_multi(chains, chains_aligned):
    for index, chain in enumerate(chains):
        print(str(index) + ': ' + chain)

    print("\nAligned:\n")

    for index, chain in enumerate(chains_aligned):
        print(str(index)  + ": " + chain)



