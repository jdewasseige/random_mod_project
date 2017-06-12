# -*- coding: utf-8 -*-
"""
Created on Tue May  16 2017

@author: john
"""
import numpy as np
from discreteMarkovChain import markovChain
np.set_printoptions(threshold=np.nan) # this line allows to print all elements of matrix

def fillMatrixWithDiceProb():
    """
    Fill the two board transition matrices following their get out of jail strategy:
    - M_DOUBLE : wait 3 times and try to make double strategy,
    - M_FINE : pay 50 euro fine and immediately get out of jail.
    """
    # number of squares
    n = 40
    # if double strategy to get out of jail (40 normal states + 3 for the jail part)
    M_double = np.zeros((n+3, n+3))
    # if 50 euro fine strategy to get out of jail (40 normal states)
    M_fine = np.zeros((n, n))
    
    # dice sum probability 2:1/36, 3:2/36, ...
    dice_prob = np.array([1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1])/36.0
    l = len(dice_prob)
    
    for i in range(40):
        # fill until dice_prob exceeds end of row
        if i < 40 - l - 1:
            M_fine[i,2+i:l+(2+i)] = dice_prob
        # fill the end of row then the beginning with the rest of dice_prob
        elif i < n-2:
            M_fine[i,2+i:n] = dice_prob[0:n-(2+i)]
            M_fine[i,0:l-n+2+i] = dice_prob[n-i-2:l]
        # fill the two last squares with dice_prob starting in columns 0 and 1
        else:
            M_fine[i,i-n+2:l+(i-n+2)] = dice_prob 
    return M_fine
    
#TODO
#def fillMatrixWithJailAndActionCommunityCardsProb(matrix):
#    TODO: Action Cards are on the fields 2,7,17,22,33
#            1 Step: Get the probability to stay on the action field probStay
#            2 Step: Calculate the probabilities to go to field x having 
#            landed on an action field p_x_fromAction
#            3 Step: For every state: multiply the probability to arrive at an 
#            action field p_arrive by probStay and add p_arrive * p_x_fromAction 
#            to all the fields x

#    probStayCommunity = ...
#     probStayAction = ...
#     for probRow in matrix:
#         for i in range(len(probRow):
##             for the community cards
#             if(i in [2,17] and not probRow[i] == 0):
#            
##             for the action cards
#             elif(i in [7,22,33] and not probRow[i] == 0):
                 
             
    
def calculateStationaryVector(matrix):
    """
    -Calculates the stationnary vector of the matrix by 
    solving the equation PI = PI * M for PI 
    - Returns the stationnary vector PI
    """
    markovCh = markovChain(matrix)
    markovCh.computePi('linear')
    return markovCh.pi

if __name__ == "__main__":
    M_fine = fillMatrixWithDiceProb()
    print(M_fine)
    print(calculateStationaryVector(M_fine))