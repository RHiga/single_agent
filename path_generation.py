import numpy as np
import copy
def path_generation(env_grid, result, start, goal, block=[-1, -1]):
    # Initialize
    env = env_grid
    value = copy.deepcopy(result)
    start_r = start[0]
    start_c = start[1]
    goal_r = goal[0]
    goal_c = goal[1]
    # Conflict of Path
    block_r = block[0]
    block_c = block[1]

    # Constrains of order side agent
    value[start_r][start_c] = 0
    value[goal_r][goal_c] = 1
    if block_r != -1:
        value[block_r][block_c] = -10

    generated_path = []
    u_value = []
    u_value.append(-value[goal_r][goal_c])
    #u_value = -value[goal_r][goal_c]

    i = 0
    #while not (start_r == goal_r and start_c == goal_c):
    for __ in range(len(value)**2):
        # Point get from value
        value[start_r][start_c] = 0
        # print('iteration', i, start_r, start_c)
        # Path memorization
        generated_path.append([start_r, start_c])

        # Value search
        v_list = np.array([-0.1, -0.1, -0.1, -0.1])
        if (0 <= start_r+1 < env.row_length):
            v_list[0] = value[start_r+1][start_c]
        if (0 <= start_r-1 < env.row_length):
            v_list[1] = value[start_r-1][start_c]
        if (0 <= start_c+1 < env.column_length):
            v_list[2] = value[start_r][start_c+1]
        if (0 <= start_c-1 < env.column_length):
            v_list[3] = value[start_r][start_c-1]
        #print('argmax', np.argmax(v_list), 'max', np.max(v_list))

        # Utility value
        #u_value += np.max(v_list)
        u_value.append(np.max(v_list))

        # Stop condition by back step
        if(np.max(v_list) == 0):
            #u_value += value[goal_r][goal_c]
            u_value.append(value[goal_r][goal_c])
            break

        # Select of Actions
        if np.argmax(v_list) == 0:
            start_r += 1
            #print('down')
        elif np.argmax(v_list) == 1:
            start_r -= 1
            #print('up')
        elif np.argmax(v_list) == 2:
            start_c += 1
            #print('right')
        elif np.argmax(v_list) == 3:
            start_c -= 1
            #print('left')

    return generated_path, u_value

def conflict(path1, path2):
    length = min(len(path1), len(path2))
    for _ in range(length):
        if path1[_] == path2[_]:
            return path2[_]
    for _ in range(length - 1):
        if path1[_:_+2] == [path2[_:_+2][1], path2[_:_+2][0]]:
            return path1[_+1] #path1[_:_+2]
