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

        self.grid2 = [
            [0, 0, 1],
            [0, -1, 0],
            [0, 0, 0]
        ]

        self.grid = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1]
        ]

        #self.grid  = [[0] * 5] * 5
        #self.grid[0][4] = 1
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
        self.y = 0
        self.x = 0
        return 1 #(self.y*3+self.x+1)

    def step(self, action):
        """
            Action: 0, 1, 2, 3
        """

        self.y = max(0, min(self.y + self.actions[action][0],4))
        self.x = max(0, min(self.x + self.actions[action][1],4))

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

class Chat(object):
    """docstring for Chat"""
    def __init__(self, y, x):
        super(Chat, self).__init__()
        self.y, self.x = y, x

    def step(self, action,env):
        """
            Action: 0 haut , 1 bas , 2 gauche , 3 droite
        """
        #env.grid[self.y][self.x] == 0
    
        

        y2 = max(0, min(self.y + env.actions[action][0],4))
        x2 = max(0, min(self.x + env.actions[action][1],4))
        print(" chat  y2,x2 : ",y2,", ",x2)
        # si la maison ne passe pas devant un mure
        if env.grid[y2][x2] != -1:

            env.grid[self.y][self.x] = 0
            self.y = y2
            self.x = x2 

            env.grid[self.y][self.x] = 1  
        print(" chat  y,x : ",self.y,", ",self.x)
        #input()
        return (self.y, self.x)

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
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
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

    chat = Chat(4, 4)
    #print("dim : ",np.ndim(env.grid))
    # # entrainement
    for _ in range(2000):
        # Reset the game
        st = env.reset()
        while not env.is_finished():
            #print("ok")
            #env.show()
            #at = int(input("$>"))
            at = take_action(st, Q, 0.4) # recuperer val max de Q

            stp1, r = env.step(at)
            #print("s", stp1)
            #print("r", r)

            # Update Q function
            atp1 = take_action(stp1, Q, 0.1)
            Q[st][at] = Q[st][at] + 0.1*(r + 0.9*Q[stp1][atp1] - Q[st][at])

            st = stp1

    for s in range(1, 26):
        print(s, Q[s]) 

    #input()
    changerC = 1

    # test
    st = env.reset()
    #j = 0
    while not env.is_finished():
        #j +=1
        #print("j : ",j)
        env.show()
        print("x,y init : ",chat.x,",",chat.y)
        if changerC:
            atM = int(input(">"))
            yM, xM = chat.step(atM, env)
            env.show()
            changerM = int(input("\n>continuer à bouger la maison ? (0/1) "))

        print("x,y : ",env.x,",",env.y)
        #at = int(input("$>"))
        at = take_action(st, Q, 0.4)

        env.step(at)
        print("action : ",at)
        print("s", stp1)
        print("r")

        #exploitation
        atp1 = take_action(stp1, Q, 0.0)
        Q[st][at] = Q[st][at] + 0.1*(r + 0.9*Q[stp1][atp1] - Q[st][at])

        st = stp1
    print("x,y : ",env.x,",",env.y)  
    env.show()