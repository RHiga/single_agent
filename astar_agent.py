import networkx as nx
import numpy as np

class Astar_Agent():

    def __init__(self, grid):

        self.grid = grid
        self.start, self.goal = self.grid_to_s_g(self.grid)
        self.g_row, self.g_column = np.shape(self.grid)
        self.path = self.astar_path()
        self.step = 0
        self.rev_step = len(self.path)

    def grid_to_s_g(self, grid):
        for i, j in enumerate(grid):
            for l, m in enumerate(j):
                if m == 2:
                    self.start = [i, l]
                elif m == 1:
                    self.goal = [i, l]
        return self.start, self.goal

    def dist(self, a, b):
        x1 = np.array(a, dtype=np.float32)
        x2 = np.array(b, dtype=np.float32)
        return np.linalg.norm(x1-x2, ord=1)

    def astar_path(self):

        # dim[x_axis, y_axis], x_axis = g_column
        G = nx.grid_graph(dim=[self.g_column, self.g_row])

        for _a, _b in enumerate(self.grid):
            for _c, _d in enumerate(_b):
                # remove obstacle node frome nodes
                if _d == 9:
                    G.remove_node((_a, _c))

        path = nx.astar_path(G, tuple(self.start), tuple(self.goal), heuristic=self.dist)
        self.path = [list(e) for e in path]
        return self.path

    def action(self):
        a_star_path = np.array(self.path)

        if((a_star_path[self.rev_step-1] == self.start)).all():
            self.step = 0
            self.rev_step = len(self.path)

        if self.step < len(self.path)-1:
            self.step += 1

            if ((a_star_path[self.step-1] + [-1, 0]) == a_star_path[self.step]).all():
                return 0
            elif ((a_star_path[self.step-1] + [1, 0]) == a_star_path[self.step]).all():
                return 1
            elif ((a_star_path[self.step-1] + [0, -1]) == a_star_path[self.step]).all():
                return 2
            elif ((a_star_path[self.step-1] + [0, 1]) == a_star_path[self.step]).all():
                return 3

        if self.step >= len(self.path)-1:
            self.step += 1
            self.rev_step -= 1
            if ((a_star_path[self.rev_step] + [-1, 0]) == a_star_path[self.rev_step-1]).all():
                return 0
            elif ((a_star_path[self.rev_step] + [1, 0]) == a_star_path[self.rev_step-1]).all():
                return 1
            elif ((a_star_path[self.rev_step] + [0, -1]) == a_star_path[self.rev_step-1]).all():
                return 2
            elif ((a_star_path[self.rev_step] + [0, 1]) == a_star_path[self.rev_step-1]).all():
                return 3

    def action_standby(self, space, stock=1):
        start = np.array(space)
        if (start == self.start).all() and (stock <=0):
            return 2
        else:
            return self.action()
