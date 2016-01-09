
import numpy as np
import generator as gen
from collections import Counter
import math as math
import functools

def estimate_posterior(alphabet, data, sequence_id, prev_positions, alpha, alpha_prime, W):
    '''
    :return: a list containing a the posterior log-probability for each position to be the starting position
    of the sequence (sequence_id) : p(r_n|R_n | D)
    '''
    N = len(data)
    M = len(data[0])
    K = len(alphabet)
    # number of background positions
    B = N*(M - W)
    pos_prob = []

    for r_i in range(M-W):
        positions = prev_positions
        positions[sequence_id] = r_i

        # Computing Bk for all k in alphabet
        background = [data[i][:positions[i]] + data[i][positions[i] + W:] for i in range(N)]
        background_counts = Counter(item for seq in background for item in seq)

        # Computing (Nkj for all k in alphabet) for all j in W
        words = [data[i][positions[i]:positions[i] + W] for i in range(N)]
        words_counts = [Counter([words[i][j] for i in range(N)]) for j in range(W)]

        # Normalizing constants
        z_background =  math.gamma((sum(alpha_prime))) / math.gamma(B*(sum(alpha_prime)))
        z_word = math.gamma((sum(alpha))) / math.gamma(N*(sum(alpha)))

        # background probabilities
        p_list = [math.log(math.gamma(background_counts[alphabet[k]] + alpha_prime[k])) - math.log(math.gamma(alpha_prime[k])) for k in range(K)]
        prob = math.log(z_background) + functools.reduce(lambda x,y : x+y, p_list)

        # magic word probabilities
        for j in range(W):
            p_list = [math.log(math.gamma(words_counts[j][alphabet[k]] + alpha[k])) - math.log(math.gamma(alpha[k])) for k in range(K)]
            p_j = math.log(z_word) * functools.reduce(lambda x,y : x+y, p_list)
            prob += p_j

        pos_prob.append(prob)

    return pos_prob

def sampler():
    # todo
    return 0 


if __name__ == '__main__':
    alphabet = ['A', 'T', 'G', 'C']
    alpha_prime = [1,1,1,1] # prior parameter for background
    alpha = [1,7,10,2] # prior parameter for magic word
    N = 5 # number of sequences
    M = 10 # sequence length
    W = 3 # magic word length

    # Generating sequences and true starting positions
    data, positions = gen.generate_sequences(alphabet, alpha, alpha_prime, N, M, W)
    prev_positions =  np.random.randint(0, M - W + 1, N)
    print(prev_positions)
    test = estimate_posterior(alphabet, data, 1, positions, alpha, alpha_prime, W)
    print(test)