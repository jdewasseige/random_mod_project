class Simulation():

    """The simulation file that can be created and run."""

    def __init__(self):
        """initialize a simulation.


        """

        self.moneyPlayer1 = 2000
        self.moneyPlayer2 = 2000

        self.fieldPlayer1 = 0
        self.fieldPlayer2 = 0

        self.costsPlayer1 = [0] * 40
        self.costsPlayer2 = [0] * 40

        # when passing at go you gain 200
        self.costsPlayer1[0] = 200
        self.costsPlayer2[0] = 200

        # player 1 owns the orange streets and all the train stations.
        self.costsPlayer2[5] = -200
        self.costsPlayer2[15] = -200
        self.costsPlayer2[25] = -200
        self.costsPlayer2[35] = -200
        self.costsPlayer2[16] = -180
        self.costsPlayer2[18] = -180
        self.costsPlayer2[19] = -200


        # player 2 owns all blue streets.
        self.costsPlayer1[1] = -60
        self.costsPlayer1[3] = -60
        self.costsPlayer1[6] = -100
        self.costsPlayer1[8] = -100
        self.costsPlayer1[9] = -120
        self.costsPlayer1[37] = -350
        self.costsPlayer1[39] = -400



        

    def run(self, nbMax):
        """Run the simulation, with a given maximal number of turns.

        :nbMax: TODO
        :returns: Owings of two players at the end.

        """
        for i in range(nbMax):
            self.fieldPlayer1 = self.getNewField(self.fieldPlayer1)
            payement = self.costsPlayer1[self.fieldPlayer1]
            self.moneyPlayer1 += payement
            if(payement < 0):
                self.moneyPlayer2 -= payement
            
            self.fieldPlayer2 = self.getNewField(self.fieldPlayer2)
            payement = self.costsPlayer2[self.fieldPlayer2]
            self.moneyPlayer2 += payement
            if(payement < 0):
                self.moneyPlayer1 -= payement

            print("fields after step", i , " : ", self.fieldPlayer1, " and " , self.fieldPlayer2)
            print("money after step", i, " : " , self.moneyPlayer1, " and ", self.moneyPlayer2)

            if(self.moneyPlayer1 < 0 or self.moneyPlayer2 < 0) :
                self.moneyPlayer1 = min(0, self.moneyPlayer1)
                self.moneyPlayer2 = min(0, self.moneyPlayer2)
                break


        return [self.moneyPlayer1, self.moneyPlayer2]
        


            
    def getNewField(self, field):
        """Returns the new field depending on the current field.
        Probabilities from the Markov chains are used here.

        :field: TODO
        :returns: TODO

        """
        newfield = field + 7
        if(newfield > 39) :
            newfield -= 40
        return newfield

if __name__ == "__main__":
    simMonop = Simulation()
    print(simMonop.run(50))
