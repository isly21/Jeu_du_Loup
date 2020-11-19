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

        self.yMaison = 0
        self.xMaison = 2

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

class Maison(object):
    """docstring for Maison"""
    def __init__(self, y, x):
        super(Maison, self).__init__()
        self.y = y
        self.x = x
        print(" position init maison y,x : ",self.y,", ",self.x)

    def step(self, action,env):
        """
            Action: 0 haut , 1 bas , 2 gauche , 3 droite
        """
        #env.grid[self.y][self.x] == 0
    
        

        y2 = max(0, min(self.y + env.actions[action][0],2))
        x2 = max(0, min(self.x + env.actions[action][1],2))
        # si la maison ne passe pas devant un mure
        if env.grid[y2][x2] != -1:

            env.grid[self.y][self.x] = 0
            self.y = y2
            self.x = x2 
            env.grid[self.y][self.x] = 1
            
        

        #print(env.grid)

        print(" maison y,x : ",self.y,", ",self.x)
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
    maison = Maison(0,2)

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
    # for _ in range(100):
    #     # Reset the game
    #     st = env.reset()
    #     while not env.is_finished():
    #         #env.show()
    #         #at = int(input("$>"))
    #         at = take_action(st, Q, 0.4) # recuperer val max de Q

    #         stp1, r = env.step(at)

            
    #         #print("s", stp1)
    #         #print("r", r)

    #         # Update Q function
    #         atp1 = take_action(stp1, Q, 0.1)
    #         Q[st][at] = Q[st][at] + 0.1*(r + 0.9*Q[stp1][atp1] - Q[st][at])

    #         st = stp1

    for s in range(1, 10):
        print(s, Q[s]) 

    changerM = 1
    # test
    for _ in range(200):
        st = env.reset()
        while not env.is_finished():
            
            #print("x,y : ",env.x,",",env.y)
            #actionM = int(input("$>"))
            #env.stepMaison(1)
            

            if changerM:
                env.show()
                print("action : ",at)
                atM = int(input(">"))
                yM, xM = maison.step(atM, env)
                
                changerM = int(input("\n>continuer à bouger la maison ?"))
            
            
            #maison.step(1,env)
            #print(env.grid)
            #input()
            at = take_action(st, Q, 0.4)

            stp1, r = env.step(at)
            
            # print("s", stp1)
            #print("r")

            # exploitation
            atp1 = take_action(stp1, Q, 0.0)
            Q[st][at] = Q[st][at] + 0.1*(r + 0.9*Q[stp1][atp1] - Q[st][at])

            st = stp1

        # st = stp1
    print("y,x : ",env.y,",",env.x)  

    for s in range(1, 10):
        print(s, Q[s]) 
    #env.show()

    #print("res",env.grid[2][2])
     # [-1, 0], # Up action 0
     #        [1, 0], #Down action 1
     #        [0, -1], # Left action 2
     #        [0, 1] # Right action 3