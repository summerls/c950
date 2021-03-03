

class truck:

    def __init__(self, id):
        self.capacity = 16
        self.currentLoad = 0
        self.speed = 18
        self.inventory = []
        self.route = []
        self.id = id
        self.miles = 0


    def load(self, packages):
        if self.currentLoad < 17:
            for i in range(len(packages)):
                self.inventory.append(packages[i])
                self.currentLoad += 1

    def getInventory(self):
        return self.inventory

    def getId(self):
        return self.id

    def deliverPackage(self, package):
        self.inventory.remove(package)