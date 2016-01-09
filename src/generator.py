
import numpy as np

"""
This script generates N sequences of length M over the alphabet, each containing a magic word of length W
"""

def sample(alphabet, categorical):
    """
    :param alphabet: the alphabet of the sequences
    :param categorical: parameter of the categorical distribution
    :return: a sample from the given categorical distribution
    """
    return alphabet[np.argmax(np.random.multinomial(1,categorical))]

def generate_sequences(alphabet, alpha, alpha_prime, N = 5, M = 7, W =3 ):
    """
    :return: a list of sequences and a list of starting positions
    """
    #background
    theta_back = np.random.dirichlet(alpha_prime)
    sequences = [[sample(alphabet, theta_back) for j in range(M)]for i in range(N)]

    #magic-word
    thetas_magic = np.random.dirichlet(alpha, W)
    positions = [np.random.randint(0, M-W+1) for i in range(N)]
    sequences = [[sample(alphabet, thetas_magic[x-pos]) if x >= pos and x < pos+W else seq[x] for x in range(len(seq))] for seq, pos in zip(sequences, positions)]

    return sequences, positions

categorical = np.ones(4)*1/4
alphabet = ['A', 'B', 'C', 'D']
alpha_prime = [1,1,1,1]
alpha = [1,5,6,2]
sequences, positions = generate_sequences(alphabet,alpha, alpha_prime)
print("sequences", sequences)
print("positions", positions)