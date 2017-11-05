import numpy as np


class GapPenaltyStrategy:

    def __init__(self, chain_a, chain_b, initial_penalty, continuous_penalty):
        self.delete_length_matrix = np.zeros((len(chain_a) + 1, len(chain_b) + 1))
        self.insert_length_matrix = np.zeros((len(chain_a) + 1, len(chain_b) + 1))
        self.initial_penalty = initial_penalty
        self.continuous_penalty = continuous_penalty

    def get_delete_gap_penalty(self, i, j):
        length = self.delete_length_matrix[i][j-1]
        return self.initial_penalty + length * self.continuous_penalty

    def get_insert_gap_penalty(self, i, j):
        length = self.insert_length_matrix[i-1][j]
        return self.initial_penalty + length * self.continuous_penalty

    def record_delete_gap_penalty(self, i, j):
        self.delete_length_matrix[i][j] = self.delete_length_matrix[i][j-1] + 1

    def record_insert_gap_penalty(self, i, j):
        self.insert_length_matrix[i][j] = self.insert_length_matrix[i-1][j] + 1