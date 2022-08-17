import numpy as np

def simple_negotiation(u1e, u2e, turn):
    ue = 'None'
    i = 0
    for _ in range(turn):
        i += 1

        a2 = u2e*np.random.rand()
        print('a2_offer', i, a2)

        if (u1e < a2):
            ue = a2
            print('Accept', a2)
            break

        a1 = np.random.rand() + u1e
        i += 1
        print('a1_offer', i, a1)
        
        if (a1 < u2e):
            ue = a1
            print('Accept', a1)
            break

    return ue
