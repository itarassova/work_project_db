class Compound:

    # Constructor that gets called when you create new instance of a class
    # Like Compound("1234-56-78", "Trinitropentosulfate")
    def __init__(self, cas, name):
        if not cas or cas.casefold() == 'N/A':
            raise ValueError("No CAS present")
        self.cas = cas
        self.name = name

    # Internal function (note the __) that returns the main key of the class
    # Relevant for functions like hash() and eq()
    def __key(self):
        return (self.cas)

    # Function that get's called when you do x == y
    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__key() == other.__key()

    # Function used to determine position in dictionaries and sets.
    # If hashes are the same for two instances, they will occupy the same slot
    def __hash__(self):
        return hash(self.__key())
