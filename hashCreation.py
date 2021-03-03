class HashCreation:

    #initialize hash table using an integer parameter to determine the size
    def __init__(self, tablesize):
        self.size = tablesize
        self.hashTable = []
        for i in range(tablesize):
            self.hashTable.append([])

    #insert a package into the hash table using its id and the hash object
    def insert(self, packageID, thing):
        with open('C:/Users/allot/Documents/c950.csv') as data:
            self.hashTable[packageID] = thing

    #set the delivery time in the hash object for the package
    def setDelivery(self, id, time):
        thing = self.hashTable[id]
        thing.set_delivery(time)

    #set the notes for the hash object in the hash table
    def setNotes(self, id, notes):
        thing = self.hashTable[id]
        thing.set_notes(notes)

    #set the truck id in the hash object for the package
    def setTruckId(self, id, truckId):
        thing = self.hashTable[id]
        thing.set_truckId(truckId)

    #set the truck load time in the hash object for the package
    def setOnTruck(self, id, time):
        thing = self.hashTable[id]
        thing.set_onTruck(time)

    #set total miles travelled to deliver the package for the truck it is being delivered by
    def setDeliveryMiles(self, id, value):
        thing = self.hashTable[id]
        thing.set_deliveryMiles(value)

    def retreiveDeliveryMiles(self, id):
        thing = self.hashTable[id]
        return thing.get_deliveryMiles()

    def retreive(self, id):
        thing = self.hashTable[id]
        return thing.get_all()

    def retreiveOnTruck(self, id):
        thing = self.hashTable[id]
        return thing.get_onTruck()

    def retreiveTruckId(self, id):
        thing = self.hashTable[id]
        return thing.get_truckId()

    def retreiveNotes(self, id):
        thing = self.hashTable[id]
        return thing.get_notes()

    def retreiveId(self):
        return self.get_Id()

    def retreiveAddress(self, id):
        thing = self.hashTable[id]
        return thing.get_address()

    def retreiveFormattedAddress(self, id):
        thing = self.hashTable[id]
        formattedAdd = thing.get_formattedAdd()
        formattedAdd = " ".join(formattedAdd)
        return formattedAdd

    def retreiveDeadline(self, id):
        thing = self.hashTable[id]
        return thing.get_deadline()

    def retreiveWeight(self, id):
        thing = self.hashTable[id]
        return thing.get_weight()

    def retriveDelivery(self, id):
        thing = self.hashTable[id]
        return thing.get_delivery()

