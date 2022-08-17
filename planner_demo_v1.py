from environment import Environment
from planner import ValueIterationPlanner
import numpy as np
from path_generation import path_generation, conflict
from simple_negotiation import simple_negotiation
import copy

p_gene = path_generation

def main():
    # Make grid environment.
    # Goal: 1
    # Block: 9
    # Danger: -1
    # Normal: 0
    grid1 = [
        [0, 9, 1, -1, -1, 9],
        [0, 9, 0, 0, 0, 9],
        [0, 9, 0, 9, 0, 9],
        [0, 9, 0, 9, 0, 9],
        [0, 0, 0, 0, 0, 0],
        [9, 0, 9, 0, 9, 0],
        [9, 0, 9, 0, 9, 0],
        [9, 0, 9, 0, 9, 0],
        [0, 0, 0, 0, 0, 0]
    ]

    grid2 = [
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

    # RL1, Learning
    env1 = Environment(grid1, move_prob=move_prob, init_colmn=5)
    planner1 = ValueIterationPlanner(env1)
    result1 = planner1.plan()

    # RL2, Learning
    env2 = Environment(grid2, move_prob=move_prob, init_colmn=3)
    planner2 = ValueIterationPlanner(env2)
    result2 = planner2.plan()

    # Path Planning, Agent1
    print('Agent1', 'Non-Negotiated path', 'Utility value')
    path1, u_v1 = p_gene(env1, result1, start=[8, 5], goal=[0, 2])
    print(path1)
    print(u_v1)

    # Path Planning, Agent2
    print('Agent2', 'Non-Negotiated path', 'Utility value')
    path2, u_v2 = p_gene(env2, result2, start=[8, 3], goal=[0, 4])
    print(path2)
    print(u_v2)

    # Conflict check
    conf_path = conflict(path1, path2)
    if conf_path == None: conf_path = [-1, -1]
    print('Blockd point:', conf_path)
    print('Agent1 state and value:', path1.index(conf_path), u_v1[path1.index(conf_path)])
    print('Agent2 state and value:', path2.index(conf_path), u_v2[path2.index(conf_path)])

    # Path Negotiated, Agent2
    print('Agent2', 'Blocked path', 'Utility value')
    path2b, u_v2b = p_gene(env2, result2, start=[8, 3], goal=[0, 4], block=conf_path)
    print(path2b)
    print(u_v2b)
    print('Agent2 new value:', u_v2b[path2.index(conf_path)])
    u2_diff = u_v2[path2.index(conf_path)] - u_v2b[path2.index(conf_path)]
    print('Utility2 diff:', u2_diff)

    # Path Negotiated, Agent1
    print('Agent1', 'Blocked path', 'Utility value')
    path1b = copy.deepcopy(path1)
    u_v1b = u_v1
    print(path1b)
    print(u_v1b)
    print(u_v1[path1.index(conf_path)], u_v1[path1.index(conf_path)-1])
    u1_diff = u_v1[path1.index(conf_path)] - u_v1[path1.index(conf_path)-1]
    print('Utility1 diff:', u1_diff)

    # Negotiation Range
    print('Negotiation:', u1_diff, '< e and e <', u2_diff)

    epsilon = simple_negotiation(u1_diff, u2_diff, 10)
    print('Negotiation results:', epsilon)

if __name__ == "__main__":
    main()
