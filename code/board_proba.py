# -*- coding: utf-8 -*-
"""
Created on Tue May  16 2017

@author: john
"""
import numpy as np
import csv
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
    rentVectorSimple = np.zeros((40,2))
    with open("simpleRentAndCostMonopoly.txt") as simpleFieldsTextFile:
        counter = 0
        for line in simpleFieldsTextFile:
            costRentList = line.split()
            rentVectorSimple[counter][0] = costRentList[0]
            rentVectorSimple[counter][1] = costRentList[1]
            counter +=1 
    return rentVectorSimple

    
def createVectorForCostAndRentOfFieldsHotels():
    rentVectorHotels = np.zeros((40,2))
    with open("hotelRentAndCostMonopoly.txt") as simpleFieldsTextFile:
        counter = 0
        for line in simpleFieldsTextFile:
            costRentList = line.split()
            rentVectorHotels[counter][0] = costRentList[0]
            rentVectorHotels[counter][1] = costRentList[1]
            counter +=1 
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
    cost = rentVectorSimple[n][0]
    rent = rentVectorSimple[n][1]
    probToLandOnField = statVectorAvg[n]
    turns = int(cost/(rent*probToLandOnField))
    return turns
    
def calculateTurnsNeededToEqualizeRentAndCostHotelOfField(n):
    statVectorAvg = createAvgStatVector()
    rentVectorHotels = createVectorForCostAndRentOfFieldsHotels()
    cost = rentVectorHotels[n][0]
    rent = rentVectorHotels[n][1]
    probToLandOnField = statVectorAvg[n]
    turns = int(cost/(rent*probToLandOnField))
    return turns
    
def calculateTurnsNeededForAllFieldsSimple():
    turnsNeededToEqualizeVectorSimple = np.zeros(40)
    rentVectorSimple = createVectorForCostAndRentOfFieldsSimple()
    for i in range(len(rentVectorSimple)):
        costAndValue = rentVectorSimple[i]
        if(not costAndValue[0] == 0):
            turnsNeededToEqualizeVectorSimple[i] = calculateTurnsNeededToEqualizeRentAndCostSimpleOfField(i)
        else:
            turnsNeededToEqualizeVectorSimple[i] = float('inf')
    return turnsNeededToEqualizeVectorSimple
    
def calculateTurnsNeededForAllFieldsHotels():
    turnsNeededToEqualizeVectorHotels = np.zeros(40)
    rentVectorHotel = createVectorForCostAndRentOfFieldsHotels()
    for i in range(len(rentVectorHotel)):
        costAndValue = rentVectorHotel[i]
        if(not costAndValue[0] == 0):
            turnsNeededToEqualizeVectorHotels[i] = calculateTurnsNeededToEqualizeRentAndCostHotelOfField(i)
        else:
            turnsNeededToEqualizeVectorHotels[i] = float('inf')
    return turnsNeededToEqualizeVectorHotels
    
def getFieldsOrderedByLowestTurnsSimple():
    turnsNeededSimple = calculateTurnsNeededForAllFieldsSimple()
    fieldsOrderedByLowestTurns = np.argsort(turnsNeededSimple)[:28]
    return fieldsOrderedByLowestTurns
            
def getFieldsOrderedByLowestTurnsHotels():
    turnsNeededHotels = calculateTurnsNeededForAllFieldsHotels()
    fieldsOrderedByLowestTurns = np.argsort(turnsNeededHotels)[:28]
    return fieldsOrderedByLowestTurns
    
def writeDataToCsvFile():
    # transition matrix fine part
    matrix_fine = makeMFine()
    statio_proba_fine = calculateStationaryVector(matrix_fine)
    with open('./csvFiles/statio_proba_fine.csv', 'w') as csvfile:
        fieldnames = ['state','proba']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(0,len(statio_proba_fine)):
            writer.writerow({'state' : i,'proba' : "{:2.2f}".format(100*statio_proba_fine[i])})
    # transition matrix double throw part
    matrix_double = makeMDoubleThrow()
    statio_proba_double = convert43statVectorTo40statVector(calculateStationaryVector(matrix_double))
    with open('./csvFiles/statio_proba_double.csv', 'w') as csvfile:
        fieldnames = ['state','proba']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(0,len(statio_proba_double)):
            writer.writerow({'state' : i,'proba' : "{:2.2f}".format(100*statio_proba_double[i])})
    # calculate turns needed simple fields
    turns_simple_array = calculateTurnsNeededForAllFieldsSimple()
    with open('./csvFiles/turns_simple.csv', 'w') as csvfile:
        fieldnames = ['state','nbTurns']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(0,len(turns_simple_array)):
            writer.writerow({'state' : i,'nbTurns' : "{:2.0f}".format(turns_simple_array[i])}) 
    # ordered fields by turns needed to equalize revenue simple case
    ordered_fields_simple_turns = getFieldsOrderedByLowestTurnsSimple()
    with open('./csvFiles/ordered_fields_simple_turns.csv', 'w') as csvfile:
        fieldnames = ['rank', 'state']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(0,len(ordered_fields_simple_turns)):
            writer.writerow({'rank' : i+1, 'state' : "{:2.0f}".format(ordered_fields_simple_turns[i])})
    # calculate turns needed all fields hotels
    turns_hotels_array = calculateTurnsNeededForAllFieldsHotels()
    with open('./csvFiles/turns_hotels.csv', 'w') as csvfile:
        fieldnames = ['state','nbTurns']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(0,len(statio_proba_double)):
            writer.writerow({'state' : i,'nbTurns' : "{:2.0f}".format(turns_hotels_array[i])})
    # ordered fields by turns needed to equalize revenue hotels case
    ordered_fields_hotels_turns = getFieldsOrderedByLowestTurnsHotels()
    with open('./csvFiles/ordered_fields_hotels_turns.csv', 'w') as csvfile:
        fieldnames = ['rank', 'state']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(0,len(ordered_fields_hotels_turns)):
            writer.writerow({'rank' : i+1, 'state' : "{:2.0f}".format(ordered_fields_hotels_turns[i])})
            

if __name__ == "__main__":
    writeDataToCsvFile()
    # print(calculateTurnsNeededForAllFieldsSimple())
    # print(getFieldsOrderedByLowestTurnsSimple())
    # print(calculateTurnsNeededForAllFieldsHotels())
    # print(getFieldsOrderedByLowestTurnsHotels())

    
