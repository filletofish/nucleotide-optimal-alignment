import numpy as np

def __load_matrix():
    f = open('blosum_62.txt', 'r')
    data = f.read()
    rows = data.split("\n")
    splitted_header = rows[0].split()
    position_dictionary = dict([(value, index) for index, value in enumerate(splitted_header)])

    length = len(position_dictionary)
    matrix = np.zeros(shape=(length, length), dtype= np.int)

    for index_1, row in enumerate(rows[1:len(rows)]):
        splitted_row = row.split()
        for index_2, value in enumerate(splitted_row[1:len(splitted_row)]):
            matrix[index_1][index_2] = np.int(int(value))

    f.close()

    return matrix, position_dictionary


def blosum_62_scoring(a, b):
    if blosum_62_scoring.__has_loaded:
        position_a = blosum_62_scoring.__position_dictionary[a]
        position_b = blosum_62_scoring.__position_dictionary[b]
        return blosum_62_scoring.__matrix[position_a][position_b]
    else:
        blosum_62_scoring.__matrix, blosum_62_scoring.__position_dictionary = __load_matrix()
        blosum_62_scoring.__has_loaded = True

        return blosum_62_scoring(a, b)

blosum_62_scoring.__has_loaded = False



print(blosum_62_scoring("M", "A"))
print(blosum_62_scoring("A", "A"))

