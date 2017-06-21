class Simulation():

    """The simulation file that can be created and run."""

    def __init__(self, iniMoney):
        """initialize a simulation.

        :iniMoney: TODO

        """
        .__init__(self)

        self._iniMoney = iniMoney
        

    def run(self, nbMax):
        """Run the simulation, with a given maximal number of turns.

        :nbMax: TODO
        :returns: TODO

        """
        for i in range(nbMax):
            field = getNewField(field)
            if field > 40:
                field -= 40;


            
    def getNewField(self, field):
        """Returns the new field depending on the current field.
        Probabilities from the Markov chains are used here.

        :field: TODO
        :returns: TODO

        """
        return newfield

