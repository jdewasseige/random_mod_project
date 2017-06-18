# -*- coding: utf-8 -*-
"""
Created on Tue May  16 2017

@author: john
"""
import numpy as np
from discreteMarkovChain import markovChain
np.set_printoptions(threshold=np.nan) # this line allows to print all elements of matrix

def fillMatrixWithDiceProb(n=40):
    """
    Fill the two board transition matrices following their get out of jail strategy:
    - M_DOUBLE : wait 3 times and try to make double strategy,
    - M_FINE : pay 50 euro fine and immediately get out of jail.
    """
    # if double strategy to get out of jail (40 normal states + 3 for the jail part)
    # if 50 euro fine strategy to get out of jail (40 normal states)
    matrix = np.zeros((n, n))
    # dice sum probability 2:1/36, 3:2/36, ...
    dice_prob = np.array([1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1])/36.0
    l = len(dice_prob)
    for i in range(40):
        if(not i == 30):
            # fill until dice_prob exceeds end of row
            if i < 40 - l - 1:
                matrix[i,2+i:l+(2+i)] = dice_prob
            # fill the end of row then the beginning with the rest of dice_prob
            elif i < n-2:
                matrix[i,2+i:n] = dice_prob[0:n-(2+i)]
                matrix[i,0:l-n+2+i] = dice_prob[n-i-2:l]
            # fill the two last squares with dice_prob starting in columns 0 and 1
            else:
                matrix[i,i-n+2:l+(i-n+2)] = dice_prob 
    return matrix
    

def fillMatrixWithActionCommunityCardsProb(matrix):
#    Action Cards are on the fields 2,7,17,22,33
#            1 Step: Get the probability to stay on the action field probStay
#            2 Step: Calculate the probabilities to go to field x having 
#            landed on an action field p_x_fromAction
#            3 Step: For every state: multiply the probability to arrive at an 
#            action field p_arrive by probStay and add p_arrive * p_x_fromAction 
#            to all the fields x
     probStayCommunity = 15/17
     probStayAction = 7/17
     for probRow in matrix:
         for i in range(len(probRow)):
##             for the community cards
             if(i in [2,17,33] and not probRow[i] == 0):
                probRow[0] += 1/17*probRow[i] #go to start
                probRow[30] += 1/17*probRow[i] #go to prison
                probRow[i] *= probStayCommunity #reduce probability to stay on the field
##             for the action cards
             elif(i in [7,22,36] and not probRow[i] == 0):
                probRow[0] += 1/17*probRow[i] #go to start
                probRow[30] += 1/17*probRow[i] #go to prison
                probRow[24] += 1/17*probRow[i] #Illinois Ave.
                probRow[11] += 1/17*probRow[i] #St. Charles Place
                probRow[39] += 1/17*probRow[i] #Boardwalk
                probRow[5] += 1/17*probRow[i] #Reading Railroad
                probRow[i-3] += 1/17*probRow[i] #3steps back
                #nearest Utility
                if(i in [7,36]):
                    probRow[12] += 1/17*probRow[i] 
                elif(i == 22):
                    probRow[28] += 1/17*probRow[i] 
                #nearest Railroad *2
                if(i == 7):
                    probRow[15] += 2/17*probRow[i] 
                elif(i == 22):
                    probRow[25] += 2/17*probRow[i] 
                elif(i == 36):
                    probRow[5] += 2/17*probRow[i] 
                probRow[i] *= probStayAction #reduce probability to stay on the field
     return matrix
     
def fillMFineWithJailProb(matrix):
    matrix[30] = matrix[10] #player has to wait one turn on JailToVisit field
    return matrix 
    
def fillMDoubleThrowJailProb(matrix):
    matrix[30][40] = 1 #go to 1st jail field if landed on goToJail
    for i in [12,14,16,18,20,22]: #get the probabilities for rolling the dice
        matrix[40][i] = 1/36
        matrix[41][i] = 1/36
        matrix[42][i] = 1/36
    matrix[40][41] = 5/6 #go to 2nd turn jail field if not successful
    matrix[41][42] = 5/6 #go to 3rd turn jail field if not successful
    matrix[42][10] = 5/6 #go to jail to visit field if not successful
    return matrix

def makeMFine():
    mFine = fillMatrixWithDiceProb()      
    mFine = fillMatrixWithActionCommunityCardsProb(mFine)
    mFine = fillMFineWithJailProb(mFine)
    return mFine
    
def makeMDoubleThrow():
    mDoubleThrow = fillMatrixWithDiceProb()
    mDoubleThrow43 = np.zeros((43, 43))
    mDoubleThrow43[:40,:40] = fillMatrixWithActionCommunityCardsProb(mDoubleThrow)
    mDoubleThrow = fillMDoubleThrowJailProb(mDoubleThrow43)
    return mDoubleThrow
    
def convert43statVectorTo40statVector(vector43):
    vector40 = np.zeros(40)
    for i in range(len(vector40)):
        if(i == 30):
            vector40[i] = vector43[i] + vector43[40] + vector43[41] + vector43[42]
        else:
            vector40[i] = vector43[i]
    return vector40
    
def calculateStationaryVector(matrix):
    """
    -Calculates the stationnary vector of the matrix by 
    solving the equation PI = PI * M for PI 
    - Returns the stationnary vector PI 
    """
    markovCh = markovChain(matrix)
    markovCh.computePi('linear')
    return markovCh.pi
    
def createVectorForCostAndRentOfFieldsSimple():
    rentVectorSimple = np.zeros(44,2)
#    TODO Read In the values: [rent][cost]
#    First40 fields + 
#    41: having bought two train fields
#    42: having bought three train fields
#    43: having bought four train fields
#    44: having bought two electricity fields
    return rentVectorSimple

    
def createVectorForCostAndRentOfFieldsHotels():
    rentVectorHotels = np.zeros(44,2)
#    TODO Read In the values: [rent][cost]
#    First40 fields + 
#    41: having bought two train fields
#    42: having bought three train fields
#    43: having bought four train fields
#    44: having bought two electricity fields
    return rentVectorHotels
    
def createAvgStatVector():
    mFine = makeMFine()
    mDoubleThrow = makeMDoubleThrow()
    mFineStatVector = calculateStationaryVector(mFine)
    mDoubleThrowStatVector = convert43statVectorTo40statVector(calculateStationaryVector(mDoubleThrow))
    return np.add(mFineStatVector, mDoubleThrowStatVector)/2
    
def calculateTurnsNeededToEqualizeRentAndCostSimpleOfField(n):
    statVectorAvg = createAvgStatVector()
    rentVectorSimple = createVectorForCostAndRentOfFieldsSimple()
    cost = rentVectorSimple[n][1]
    rent = rentVectorSimple[n][0]
    probToLandOnField = statVectorAvg[n]
    turns = int(cost/(rent*probToLandOnField))
    return turns
    
def calculateTurnsNeededToEqualizeRentAndCostHotelOfField(n):
    statVectorAvg = createAvgStatVector()
    rentVectorHotels = createVectorForCostAndRentOfFieldsHotels()
    cost = rentVectorHotels[n][1]
    rent = rentVectorHotels[n][0]
    probToLandOnField = statVectorAvg[n]
    turns = int(cost/(rent*probToLandOnField))
    return turns

if __name__ == "__main__":
    print(createAvgStatVector())

    