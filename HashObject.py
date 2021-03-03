from clock import clock

class HashObject:


    def __init__(self, id, address, city, state, zipcode, deadline, kiloMass, notes):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.kiloMass = kiloMass
        self.notes = notes
        self.hashTable = []
        self.delivery = 0
        self.onTruck = 0
        self.truckId = 0
        self.deliveryMiles = 0.0


    def get_zip(self):
        return self.zipcode

    def get_all(self):
        attList = [self.id, self.address, self.city, self.state, self.zipcode, self.deadline, self.kiloMass, self.notes]
        return attList

    def get_id(self):
        return self.id

    def get_address(self):
        return self.address

    def get_deadline(self):
        return self.deadline

    def get_weight(self):
        return self.kiloMass

    def get_formattedAdd(self):
        list = [self.address, self.city, self.state, self.zipcode]
        return list

    def get_notes(self):
        return self.notes

    def get_id(self):
        return self.id

    def get_onTruck(self):
        return self.onTruck

    #set delivery time
    def set_delivery(self, time):
        timeString = str(time.getTime())
        self.delivery = timeString

    def set_notes(self, notes):
        self.notes = notes

    def set_deliveryMiles(self, miles):
        self.deliveryMiles = miles

    #get delivery time
    def get_delivery(self):
        return self.delivery

    def get_deliveryMiles(self):
        return self.deliveryMiles

    def get_truckId(self):
        return self.truckId

    #set time that the package was loaded onto a truck
    def set_onTruck(self, time):
        timeString = str(time.getTime())
        self.onTruck = timeString

    def set_truckId(self, id):
        self.truckId = id