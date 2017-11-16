import numpy as np
from Bio import SeqIO
from io import StringIO
from Source.NucleotideChain import NucleotideChain


def read_input(data):
    records = SeqIO.parse(StringIO(data), "fasta")
    return [NucleotideChain(record.id, np.array(record.seq)) for record in records]


def print_output(name_chain_a, name_chain_b, aligned_chain_seq_a, aligned_chain_seq_b, score):
    print("Score: ", score)
    print(name_chain_a)
    print(name_chain_b)
    print(aligned_chain_seq_a)
    print(aligned_chain_seq_b)