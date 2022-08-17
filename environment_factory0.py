from enum import Enum
import numpy as np


class State():

    def __init__(self, row=-1, column=-1, agv_stock=0, stock=0, in_product=0):
        self.row = row
        self.column = column
        self.agv_stock = agv_stock
        self.stock = stock
        self.in_product = in_product
    def __repr__(self):
        return "<State: [{}, {}, {}, {}, {}]>".format(self.row, self.column,
        self.agv_stock, min(self.stock, 1), min(self.in_product, 1))

    def clone(self):
        return State(self.row, self.column,
        self.agv_stock, min(self.stock, 1), min(self.in_product, 1))

    def __hash__(self):
        return hash((self.row, self.column,
        self.agv_stock, min(self.stock, 1), min(self.in_product, 1)))

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column


class Action(Enum):
    UP = 1
    DOWN = -1
    LEFT = 2
    RIGHT = -2
    #STOP = 3 #add new action
    #STOPP = -3

class Assembly():
    # Assembly agent class, gaussian type

    def __init__(self, mu=10, sigma=1):
        self.stock = 0
        self.mu = mu
        self.sigma = sigma
        self.time = 0
        self.working_time = 0
        self.product = 0
        self.product_all = 0
        self.jobp = True

    # assembly agent model
    def work(self):
        self.time +=1
        self.product = 0
        if self.jobp:
            if self.stock > 0:
                self.stock -= 1
                self.working_time = self.time + np.random.normal(self.mu, self.sigma)
                self.jobp = False
        else:
            if self.time >= self.working_time+1:
                self.product = 1
                self.product_all += 1
                self.jobp = True
                # initialization of time
                self.time = 0
        return self.product

    # stock model add
    def stock_add(self, stock=0):
        self.stock += stock
        return self.stock
    # stock model get
    def stock_get(self, stock=0):
        if self.stock > 0:
            self.stock -= stock
        return self.stock

    # product model add
    def product_stock_add(self, product=0):
        self.product_all += product
        return self.product_all

    # product model get
    def product_stock_get(self, product=0):
        if self.product_all > 0:
            self.product_all -= product
        return self.product_all

    def reset(self):
        self.time = 0
        self.product = 0
        self.stock = 0
        self.product_all = 0
        #return self.time, self.product, self.stock

class Environment():

    def __init__(self, grid, move_prob=1):
        # grid is 2d-array. Its values are treated as an attribute.
        # Kinds of attribute is following.
        #  0: ordinary cell
        #  -1: damage cell (game end)
        #  1: goal point, put stock
        #  2: start point, get stock
        #  9: block cell (can't locate agent)
        self.grid = grid
        self.agent_state = State()

        # Default reward is minus. Just like a poison swamp.
        # It means the agent has to reach the goal fast!
        self.default_reward = -0.04

        # Agent can move to a selected direction in move_prob.
        # It means the agent will move different direction
        # in (1 - move_prob).
        self.move_prob = move_prob

        # start point
        self.init_row = self.grid_to_s_g(grid)[0][0] #init_row
        self.init_colmn = self.grid_to_s_g(grid)[0][1] #init_colmn

        # Assumbly agant model output
        self.assembly = Assembly()

        # Assembly agent mode input
        self.assembly_in = Assembly()

        # agv agent stock
        self.agv_stock = 0

        # total time
        self.total_time = 0

        self.reset()


    def grid_to_s_g(self, grid):
        for i, j in enumerate(grid):
            for l, m in enumerate(j):
                if m == 2:
                    self.start = [i, l]
                elif m == 1:
                    self.goal = [i, l]
        return self.start, self.goal

    @property
    def row_length(self):
        return len(self.grid)

    @property
    def column_length(self):
        return len(self.grid[0])

    @property
    def actions(self):
        return [Action.UP, Action.DOWN,
                Action.LEFT, Action.RIGHT]#, Action.STOP, Action.STOPP] # add STOP action

    @property
    def actions_length(self):
        return len(Action)

    @property
    def states(self):
        states = []
        for _stock in range(2): # add stock loop
            for row in range(self.row_length):
                for column in range(self.column_length):
                    # Block cells are not included to the state
                    if self.grid[row][column] != 9:
                        states.append(State(row, column, _stock))
        return states

    def transit_func(self, state, action):
        transition_probs = {}
        if not self.can_action_at(state):
            # Already on the terminal cell.
            return transition_probs

        opposite_direction = Action(action.value * -1)

        for a in self.actions:
            prob = 0
            if a == action:
                prob = self.move_prob
            elif a != opposite_direction:
                prob = (1 - self.move_prob) / 2

            next_state = self._move(state, a)
            if next_state not in transition_probs:
                transition_probs[next_state] = prob
            else:
                transition_probs[next_state] += prob

        return transition_probs

    def can_action_at(self, state):
        if self.grid[state.row][state.column] == 0:
            return True
        elif self.grid[state.row][state.column] == 2:
            return True
        elif self.grid[state.row][state.column] == 1:
            return True
        else:
            return False

    def _move(self, state, action):
        if not self.can_action_at(state):
            raise Exception("Can't move from here!")

        next_state = state.clone()

        # Execute an action (move).
        if action == Action.UP:
            next_state.row -= 1
        elif action == Action.DOWN:
            next_state.row += 1
        elif action == Action.LEFT:
            next_state.column -= 1
        elif action == Action.RIGHT:
            next_state.column += 1

        # Check whether a state is out of the grid.
        if not (0 <= next_state.row < self.row_length):
            next_state = state
        if not (0 <= next_state.column < self.column_length):
            next_state = state

        # Check whether the agent bumped a block cell.
        if self.grid[next_state.row][next_state.column] == 9:
            next_state = state

        return next_state

    # Under update for Facutory Automation
    def reward_func(self, state):
        reward = 0
        reward = self.default_reward

        # run asseymbly workers, input
        self.assembly_in.work()
        #self.assembly.work()


        # reward function in Factory
        #reward = self.column_length*self.assembly.product \
        #- self.assembly.stock - self.assembly_in.product_all


        done = False
        # Check an attribute of next state. => to _move
        attribute = self.grid[state.row][state.column]
        if attribute == 1:
            done = False
        elif attribute == -1:
            # Get damage! and the game ends.
            reward += -1
            done = True
        elif attribute == 2:
            done = False

        # add stock state
        attribute = self.grid[state.row][state.column]
        if attribute == 1:
            if self.agv_stock > 0:
                self.assembly.stock_add(1)
                self.agv_stock -= 1

                reward += self.column_length
        elif attribute == 2:
            if 0 <= self.agv_stock < 1:
                if self.assembly_in.product_all > 0:
                    # Get stock
                    self.assembly_in.product_stock_get(1)
                    self.agv_stock += 1

                    reward += self.column_length

        # run asseymbly workers, output
        # self.assembly_in.work()
        self.assembly.work()

        # reward function in Factory
        reward += self.column_length*self.assembly.product \
        -(self.assembly.stock+self.assembly_in.product_all+self.agv_stock)

        # reward function in Factory, update

        weight = 5 # 10
        reward /= (weight-1)*self.column_length*3

        # Time counting
        self.total_time += 1
        if self.total_time == 2*weight*(self.column_length-1):
            done = True
            #self.total_time = 0
        return reward, done

    def reset(self):

        # Assembly agnet reset, output(right assembly agent)
        self.assembly = Assembly(mu=(self.column_length-2)*2, sigma=1)
        self.assembly.stock_add(0)

        # Assembly agent reset, input(left assembly agent)
        self.assembly_in = Assembly(mu=(self.column_length-2)*2, sigma=1)
        self.assembly_in.stock_add(100)
        #self.assembly_in.product_stock_add(1)

        # agv's initial stock
        self.agv_stock = 1

        # time count
        self.total_time = 0

        # Locate the agent
        self.agent_state = State(self.init_row, self.init_colmn, self.agv_stock,
         min(self.assembly.stock, 1), min(self.assembly_in.product_all, 1))

        return self.agent_state

    def step(self, action):
        next_state, reward, done = self.transit(self.agent_state, action)
        if next_state is not None:
            self.agent_state = next_state

        return next_state, reward, done

    def transit(self, state, action):
        transition_probs = self.transit_func(state, action)
        if len(transition_probs) == 0:
            return None, None, True

        next_states = []
        probs = []
        for s in transition_probs:
            next_states.append(s)
            probs.append(transition_probs[s])

        next_state = np.random.choice(next_states, p=probs)
        reward, done = self.reward_func(next_state)


        # add next state, agv_state and assembly state
        next_state.agv_stock = self.agv_stock
        next_state.stock = self.assembly.stock
        next_state.in_product = self.assembly_in.product_all

        return next_state, reward, done
