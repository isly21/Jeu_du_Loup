import numpy as np
from random import randint
import random
import pygame
class EnvGrid(object):
    """
        docstring forEnvGrid.
    """
    def __init__(self):
        super(EnvGrid, self).__init__()

        self.grid = [
            [0, 0, 1],
            [0, -1, 0],
            [0, 0, 0]
        ]
        # Starting position
        self.y = 2
        self.x = 0

        self.actions = [
            [-1, 0], # Up action 0
            [1, 0], #Down action 1
            [0, -1], # Left action 2
            [0, 1] # Right action 3
        ]

    def reset(self):
        """
            Reset world
        """
        self.y = 2
        self.x = 0
        return (self.y*3+self.x+1)

    def step(self, action):
        """
            Action: 0, 1, 2, 3
        """

        self.y = max(0, min(self.y + self.actions[action][0],2))
        self.x = max(0, min(self.x + self.actions[action][1],2))

        return (self.y*3+self.x+1) , self.grid[self.y][self.x]

    def show(self):
        """
            Show the grid
        """
        print("---------------------")
        y = 0
        for line in self.grid:
            x = 0
            for pt in line:
                print("%s\t" % (pt if y != self.y or x != self.x else "X"), end="")
                x += 1
            y += 1
            print("")

    def is_finished(self):
        return self.grid[self.y][self.x] == 1

def take_action(st, Q, eps):
    # Take an action
    if random.uniform(0, 1) < eps:
        action = randint(0, 3)
    else: # Or greedy action
        action = np.argmax(Q[st]) 
        # print("action : ", np.argmax(Q[st]))
        # print("Q[st] : ",Q[st], "\n")

    return action

if __name__ == '__main__':
    env = EnvGrid()
    st = env.reset()

    Q = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
    ]

    # entrainement
    for _ in range(100):
        # Reset the game
        st = env.reset()
        while not env.is_finished():
            #env.show()
            #at = int(input("$>"))
            at = take_action(st, Q, 0.4) # recuperer val max de Q

            stp1, r = env.step(at)
            #print("s", stp1)
            #print("r", r)

            # Update Q function
            atp1 = take_action(stp1, Q, 0.0)
            Q[st][at] = Q[st][at] + 0.1*(r + 0.9*Q[stp1][atp1] - Q[st][at])

            st = stp1

    for s in range(1, 10):
        print(s, Q[s]) 

    # test
    st = env.reset()
    while not env.is_finished():
        env.show()
        print("x,y : ",env.x,",",env.y)
        #at = int(input("$>"))
        at = take_action(st, Q, 0.4)

        env.step(at)
        print("action : ",at)
        # print("s", stp1)
        #print("r")

        # exploitation
        #atp1 = take_action(stp1, Q, 0.0)
        #Q[st][at] = Q[st][at] + 0.1*(r + 0.9*Q[stp1][atp1] - Q[st][at])

        # st = stp1
    print("x,y : ",env.x,",",env.y)  
    env.show()