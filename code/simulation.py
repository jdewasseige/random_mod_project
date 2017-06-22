import numpy as np
import random
import board_proba 
np.set_printoptions(threshold=np.nan)

class Simulation():

    """The simulation file that can be created and run."""

    def __init__(self):
        """initialize a simulation.
        """

        self.costsPlayer1 = [0] * 43
        self.costsPlayer2 = [0] * 43
        
        #tax field at spot number 4
        self.costsPlayer1[4] = -200
        self.costsPlayer2[4] = -200
        
        #tax field at spot number 38
        self.costsPlayer1[38] = -200
        self.costsPlayer2[38] = -200
        
        #in the beginnig there is freeparking = 50 
        self.freeparking = 50
        

        # player 1 has hotels on the orange streets and owns all the train stations.
        self.costsPlayer2[5] = -200
        self.costsPlayer2[15] = -200
        self.costsPlayer2[25] = -200
        self.costsPlayer2[35] = -200
        self.costsPlayer2[16] = -950
        self.costsPlayer2[18] = -950
        self.costsPlayer2[19] = -1000

        # player 2 owns all light blue streets, all brown streets and has hotels
#        on the dark blue streets.
        self.costsPlayer1[1] = -60
        self.costsPlayer1[3] = -60
        self.costsPlayer1[6] = -100
        self.costsPlayer1[8] = -100
        self.costsPlayer1[9] = -120
        self.costsPlayer1[37] = -1500
        self.costsPlayer1[39] = -2000



        

    def run(self, nbMax, matrix):
#        init
        self.moneyPlayer1 = 2000
        self.moneyPlayer2 = 2000
        self.fieldPlayer1 = 0
        self.fieldPlayer2 = 0
        
        if(len(matrix[0]) == 40):
#           if jail matrix is used -50
            self.costsPlayer1[30] = -50
            self.costsPlayer2[30] = -50
            
        """Run the simulation, with a given maximal number of turns.

        :nbMax: max Amount of turns played until players decide to accept draw
        :returns: Owings of two players at the end.

        """
        for i in range(nbMax):
            self.fieldPlayer1, wentOverGo = self.getNewField(self.fieldPlayer1, matrix)
            self.moneyPlayer1 += self.checkFieldForSpecialPayment(self.fieldPlayer1)
            if(wentOverGo):
                self.moneyPlayer1 += 200
            payement = self.costsPlayer1[self.fieldPlayer1]
            self.moneyPlayer1 += payement
            if(payement < 0):
                self.moneyPlayer2 -= payement
            
            self.fieldPlayer2, wentOverGo = self.getNewField(self.fieldPlayer2, matrix)
            self.moneyPlayer2 += self.checkFieldForSpecialPayment(self.fieldPlayer2)
            if(wentOverGo):
                self.moneyPlayer2 += 200
            payement = self.costsPlayer2[self.fieldPlayer2]
            self.moneyPlayer2 += payement
            if(payement < 0):
                self.moneyPlayer1 -= payement

#            print("Fields after step ", i , "(1 and 2) : ", self.fieldPlayer1, " and " , self.fieldPlayer2)
#            print("Money after step", i, "(1 and 2)  : " , self.moneyPlayer1, " and ", self.moneyPlayer2)
#            print("-------------------------------------------------------")
#            
            if(self.moneyPlayer1 < 0 or self.moneyPlayer2 < 0) :
                self.moneyPlayer1 = max(0, self.moneyPlayer1)
                self.moneyPlayer2 = max(0, self.moneyPlayer2)
                if(self.moneyPlayer1 == 0):
                    string = "1"
                else:
                    string = "2"
                print("Player",string, "is broke and the game ended after",2*i, "turns.")
                break
        return [self.moneyPlayer1, self.moneyPlayer2]
        
    def checkFieldForSpecialPayment(self, field):
        if(field == 20):
            gain = max(50,self.freeparking)
            self.freeparking = 0
            return gain
        elif(field == 4):
            self.freeparking += 200
            return 0
        elif(field == 38):
            self.freeparking += 100
            return 0
        else:
            return 0
             
    def getNewField(self, fieldBefore, matrix):
        wentOverGo = False
        vectorAfterTransition = matrix[fieldBefore]
        fieldAfter = self.getVectorAfter(vectorAfterTransition)
#        check whether player went over go and if went to prison
        if(fieldAfter <= fieldBefore and not fieldBefore == 30):
            wentOverGo = True
        return fieldAfter, wentOverGo

    def getVectorAfter(self, vectorBefore):
        randomNumberBetween0And1 = random.random()
        threshold = 0
        idx = -1
        while(threshold <= randomNumberBetween0And1):
            idx += 1
            probOfField = vectorBefore[idx]
            threshold = self.changeThreshold(probOfField,threshold)
        return idx
            
    def changeThreshold(self, probOfField,threshold):
        if(not probOfField == 0):
                threshold += probOfField
        return threshold
        
    def getStatisticForSimulation(self,n, matrix):
        player1 = player2 = draw = 0
        for i in range(n):
            result = simMonop.run(500,matrix)
            if(result[0] == 0):
                player2 += 1
            elif(result[1] == 0):
                player1 += 1
            else:
                draw += 1
        return [player1/(player1 + player2+draw), player2/(player1 + player2+draw), draw/(player1 + player2+draw)]

if __name__ == "__main__":
    simMonop = Simulation()
    
#    PICK MATRIX
#------------------------------------------
    matrix = board_proba.makeMDoubleThrow()
#    matrix = board_proba.makeMFine()
    
#    RUN STATISTIC -> COMMENT OUT LINES 89 - 91 TO AVOID PRINT OUT OVERLOAD
#------------------------------------------
    statistic = simMonop.getStatisticForSimulation(1000,matrix)
    print("------------| Player 1 wins | Player 2 wins | draw  |-------------")
    print("------------|",statistic[0],"        |",statistic[1],"        |",statistic[2],"|--------------")
    
#   PLAY ONE GAME -> UNCOMMENT LINES 89 - 91 TO SEE GAME HISTORY
#------------------------------------------
#    result = simMonop.run(500,matrix)
#    print("The final money distribution is: ")
#    print("---------------| Player 1:",result[0]," | Player 2:",result[1]," |-------------")
#    

