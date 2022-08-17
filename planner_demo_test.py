from environment import Environment
from planner import ValueIterationPlanner
import numpy as np


def main():
    # Make grid environment.
    grid = [
        [0, 9, -1, -1, 1, 9],
        [0, 9, 0, 0, 0, 9],
        [0, 9, 0, 9, 0, 9],
        [0, 9, 0, 9, 0, 9],
        [0, 0, 0, 0, 0, 0],
        [9, 0, 9, 0, 9, 0],
        [9, 0, 9, 0, 9, 0],
        [9, 0, 9, 0, 9, 0],
        [0, 0, 0, 0, 0, 0]
    ]
    move_prob = 0.9  # default value
    env = Environment(grid, move_prob=move_prob, init_colmn=3)
    planner = ValueIterationPlanner(env)

    result = planner.plan()
    np.savetxt('value.txt', result)

    # Constrains of Value
    start_r = 8
    start_c = 3
    goal_r = 0
    goal_c = 4
    block_r = 4
    block_c = 4


    # Path and Utility Generator
    result[start_r][start_c] = -10
    result[goal_r][goal_c] = 10
    # block test
    result[block_r][block_c] = -10
    # Path generation test

    i = 0
    while not (start_r == goal_r and start_c == goal_c):
        i += 1
        print(start_r, start_c)
        result[start_r][start_c] = 0
        print('iteration', i, start_r, start_c)

        v_list = np.array([-0.1, -0.1, -0.1, -0.1])
        if (0 <= start_r+1 < env.row_length):
            v_list[0] = result[start_r+1][start_c]
        if (0 <= start_r-1 < env.row_length):
            v_list[1] = result[start_r-1][start_c]
        if (0 <= start_c+1 < env.column_length):
            v_list[2] = result[start_r][start_c+1]
        if (0 <= start_c-1 < env.column_length):
            v_list[3] = result[start_r][start_c-1]

        print('argmax', np.argmax(v_list), 'max', np.max(v_list))
        if np.argmax(v_list) == 0:
            start_r += 1
            print('down')
        elif np.argmax(v_list) == 1:
            start_r -= 1
            print('up')
        elif np.argmax(v_list) == 2:
            start_c += 1
            print('right')
        elif np.argmax(v_list) == 3:
            start_c -= 1
            print('left')

if __name__ == "__main__":
    main()
