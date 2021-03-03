#Summer Schinagl #000930757

#imports
import csv
#hashCreation and hashObject are for the hash table that will contain the package data
from hashCreation import HashCreation
from HashObject import HashObject
#truck object to track trucks and inventory of trucks
from truck import truck
#clock object to track time as packages are delivered
from clock import clock

#list of delivered packages
deliveredPackages = []

#create a clock object for truck 1 and truck 2
time1 = clock()
time2 = clock()

#variable to track how many rows are in the csv document, in order to create an appropriately sized hash table
size = 0
#read the csv document for package data to count the rows and create the hash table
with open('./csv/c950.csv') as data:
    data_read = csv.reader(data, delimiter = ',')
    for row in data_read:
        size += 1
ht = HashCreation(size)

#3 lists: one for packages with special notes, one for packages that have a deadline, and one for all other packages
specialPackages = []
normalPackages = []
deadlinePackages = []

#declaring two strings to use for csv read
newString = ""

#read in the csv document for package data, skipping the first row and adding the data to the hashtable
with open('./csv/c950.csv') as data:
    first = True
    data_read = csv.reader(data, delimiter=";")
    for row in data_read:
        if not first:
            newString = " ".join(str(word) for word in row)
            rowList = newString.split(',')
            #variable for packageid for insertion into hashtable
            packageId2 = int(rowList[0])
            for item in rowList:
                newString = str(rowList[0])
                if len(rowList) < 8:
                    rowList.append("")
                #create hash object
                newObj = HashObject(int(rowList[0]), rowList[1], rowList[2], rowList[3], rowList[4], rowList[5], rowList[6], str(rowList[7]))
                #insert the object into the hashtable
                ht.insert(packageId2, newObj)
            #place the packageID of any packages with deadlines into the deadlinepackages list
            if rowList[5] != "EOD" and len(rowList[7]) ==0:
                packageId = int(rowList[0])
                deadlinePackages.append(newObj.get_id())
            #place the packageID of any packages with special notes into the specialpackages list
            if len(rowList[7]) != 0:
                packageId = int(rowList[0])
                specialPackages.append(newObj.get_id())
            #place the packageID of any packages that do not have special notes or deadlines into the normal packageslist
            if rowList[5] == "EOD" and len(rowList[7])==0:
                normalPackages.append(newObj.get_id())
        #if first iteration, skip first line of csv file by simply setting first= false
        else:
            first = False

#format function to remove spaces, commas, and quotations
def format(word):
    newWord = ""
    for digit in word:
        if digit != " " and digit != ";" and digit != '"' and digit != "'" and digit!= "[" and digit != "]":
            newWord += digit
    return newWord

#create the distance dictionary
distDict = {}
#variables to keep track of rather first or second iteration
first = True
second = False
#a simple counter to use with the location reference list
counterDist = 0
#the location reference list will be used to identify what index corresponds with what address in the distance dictionary
locReferenceList = []
#list that will contain the distances that will be added to the distDict using addressess as keys
newRowFloatList = []
#read in the csv document for the distance table, skipping the first row and adding the data to a dictionary
with open('./csv/distance.csv', encoding="utf8") as data:
    data_read = csv.reader(data, delimiter = ';')
    for row in data_read:
        #if the row is not the first or second, the data will go into the distance dictionary
        if not first and not second:
            #format in order to remove misc characters from csv import
            newRowString = format(str(row))
            newRowList = newRowString.split(",")

            #clean up list by removing any items that do not contain numbers
            for item in newRowList:
                noNumbers = True
                for i in range(0 , 9):
                    if str(i) in item:
                        noNumbers = False
                if noNumbers:
                    newRowList.remove(item)

            #clear the float version of the list to clear previous iteration and then convert the string list to a list of floats
            newRowFloatList.clear()
            for distance in newRowList:
                newRowFloatList.append(float(distance))

            #assign list of floats to the distance dictionary entry corresponding to the reference list item with its index matching the counter
            distDict[locReferenceList[counterDist]] = newRowFloatList[:]
            counterDist += 1

        #if second, set second to false and essentially skip the second row
        if second:
            second = False

        #if the row is the first, add the values to a reference list for lookup purposes
        if first:
            newString = " ".join(str(thing) for thing in row)
            rowList = newString.split('%')

            for thing in rowList:
                #add the data from the first header row into a list to use as a reference
                locReferenceList.append(thing)

            first = False
            second = True

#a simplified locRefList that will only contain the street numbers for corresponding index lookup
simplifiedLocationReferenceList = []
def locationRefSimp():

    for thing in locReferenceList:
        string = ""
        bool1 = False
        for digit in thing:
            if digit.isdigit():
                string += digit
                bool1 = True
            if not digit.isdigit():
                if bool1:
                    break

        simplifiedLocationReferenceList.append(string)

#function to find index of given node in the reference list using the street number in the address
def findNodeIndex(node):
    nodeList = []
    nodeList = node.split(" ")
    for thing in nodeList:
        if thing in simplifiedLocationReferenceList:
            return(simplifiedLocationReferenceList.index(thing))


#function to find nearest node from given node
visitedLocations =[]
def computeRoute(locIndex):
    #a location index of zero is the hub
    currentSmallest = 1000
    firstIteration = True
    indexOfSmallest = int(0)
    while len(visitedLocations) <= (len(distDict) - 2):
        #if i is zero, that is the hub index, so that would be the first iteration of the route
        for i in range(len(distDict)):
            if i ==0:
                firstIteration = True
            if not firstIteration:
                #get the list of values associated with a specific address in the distance dictionary, using the location reference list and corresponding index
                valueList = distDict[locReferenceList[i]]
                #a check to ensure no index out of bounds error results
                if len(valueList)-1 > locIndex:
                    value = valueList[locIndex]
                    if value != 0 and value !=0.0:
                        if value < currentSmallest:
                            if i not in visitedLocations:
                                #if the index i isn't already a visited index, make its distance the current smallest
                                currentSmallest = value
                                indexOfSmallest = int(i)
            #if the first iteration of the loop
            if firstIteration:
                valueList = distDict[locReferenceList[i]]
                #if the distance is not 0 or 0.0, make it current smallest, else, make the preceding value the current smallest distance
                #this is done to avoid having 0 always assigned as the current smallest, because a value of zero indicates that is the current node being traveled from
                if len(valueList)-1 > int(locIndex):
                        value =valueList[locIndex]
                        if value != 0 and value != 0.0:
                            currentSmallest = value
                            indexOfSmallest = i
                            firstIteration = False
                        else:
                            currentSmallest = valueList[locIndex+1]

        #search the table reverse in order to find all distances and return the lowest distance
        otherIndex = greedyReverseSearch(locIndex)
        #compare the lowest distance from the reverse search to the distance from the greedy search and find smallest that isn't already in the visited locations list
        if otherIndex not in visitedLocations and otherIndex < indexOfSmallest:
            indexOfSmallest = otherIndex

        #append smallest distance index to visitedLocations list
        visitedLocations.append(indexOfSmallest)
        locIndex = int(indexOfSmallest)

    #add last remaining location to end of visitedLocations list
    for m in range(len(locReferenceList)+1):
        if m != 0 and m not in visitedLocations:
            visitedLocations.append(m)


#function to search the distance table reverse
def greedyReverseSearch(node):
    valueList = distDict[locReferenceList[node]]
    firstIteration = True
    indexOfSmallest = 1000
    for value in valueList:
        if firstIteration:
            if  value != 0 and value != 0.0 and valueList.index(value) not in visitedLocations:
                currentSmallest = value
                firstIteration = False
        else:
            if value != 0 and value != 0.0:
                if currentSmallest > value:
                    if valueList.index(value) not in visitedLocations:
                        currentSmallest = value
                        indexOfSmallest = int(valueList.index(value))
    return indexOfSmallest

sortedPackages = []
truck1 = truck(1)
truck2 = truck(2)

#sort packages according to delivery order
def packageSort():
    #begin with the packages that have deadlines
    for location in visitedLocations:
        for package in deadlinePackages:
            address = ht.retreiveAddress(package)
            index = findNodeIndex(address)
            if index == location and package not in sortedPackages:
                sortedPackages.append(package)
        for package in normalPackages:
            address = ht.retreiveAddress(package)
            index = findNodeIndex(address)

            if index == location and package not in sortedPackages:
                sortedPackages.append(package)
        for package in specialPackages:
            address = ht.retreiveAddress(package)
            index = findNodeIndex(address)

            if index == location and package not in sortedPackages:
                sortedPackages.append(package)

#a list to track packages that have been loaded onto a truck
loadedPackages = []
#a list to track packages scheduled for loading onto a truck
packagesToLoad = []

def load(truck, time):
    #if there are still packages left to deliver
    if len(deliveredPackages) != len(sortedPackages):
        packagesToLoad.clear()
        if(truck.getId() ==1):
            hoursNow = time1.getHour()
            minutesNow = time1.getMinute()

        if(truck.getId() ==2):
            hoursNow = time2.getHour()
            minutesNow = time2.getMinute()

        for package in sortedPackages:
            #if package has not been loaded onto a truck
            if package not in loadedPackages:
            #a truck only has the capacity for 16 packages
                if len(packagesToLoad)<16:
                    #package 30 must be delivered before 1030 and package 1 is going to the same address
                    if package == 1:
                        if len(packagesToLoad)<15:
                            packagesToLoad.append(30)
                            loadedPackages.append(30)
                            packagesToLoad.append(1)
                            loadedPackages.append(1)
                            if truck.getId() == 1:
                                ht.setOnTruck(30, time1)
                                ht.setTruckId(30, 1)
                            if truck.getId() == 2:
                                ht.setOnTruck(30, time2)
                                ht.setTruckId(30, 2)

                    #if the package next set to deliver is 6, ensure it is after 0905 since the package wont arrive until then
                    if package ==6:
                        if hoursNow > 9:
                            if minutesNow > 5:
                                packagesToLoad.append(6)
                                loadedPackages.append(6)

                    #only load package 3 onto truck 2
                    if package == 3:
                       if truck.getId()== 2:
                            packagesToLoad.append(3)
                            loadedPackages.append(3)
                            ht.setTruckId(3, 2)
                    #only load package 18 onto truck 2
                    if package == 18:
                        if package not in loadedPackages:
                            if truck.getId() == 2:
                                packagesToLoad.append(18)
                                loadedPackages.append(18)
                                ht.setTruckId(18, 2)
                    #package 38 must be delivered on truck 2, but both 37 and 38 are going to the same address
                    if package == 37 or package == 38:
                        if package not in loadedPackages:
                            if truck.getId() == 2 and len(packagesToLoad)<15:
                                if 37 not in loadedPackages:
                                    packagesToLoad.append(37)
                                    loadedPackages.append(37)
                                    ht.setTruckId(38, 2)
                                if 38 not in loadedPackages:
                                    packagesToLoad.append(38)
                                    loadedPackages.append(38)
                                    ht.setTruckId(38, 2)
                    #if the package is 9, ensure it wont be delivered until the address has been corrected, which wont happen until 1020
                    if package == 9:
                        if package not in deliveredPackages:
                            if hoursNow > 10:
                                packagesToLoad.append(9)
                                loadedPackages.append(9)
                            if hoursNow == 10:
                                if minutesNow >=20:
                                    packagesToLoad.append(9)
                                    loadedPackages.append(9)

                        #if package is 3, it must be delivered on truck 2
                    if package == 3:
                        if len(packagesToLoad) < 15:
                            if truck.getId() ==2:
                                packagesToLoad.append(3)
                                loadedPackages.append(3)

                    #deliver 13, 15, 19, 20, 21, 34, and 39 together
                    if package == 13  or package == 15 or package == 19 or package == 20 or package == 21 or package == 34 or package == 39 or package ==14 or package ==16:
                        if len(loadedPackages) < 7:
                            if package not in loadedPackages:
                                relatedPackages = [15, 16, 13, 39, 19, 20, 21, 34, 14]
                                for relatedPackage in relatedPackages:
                                    packagesToLoad.append(relatedPackage)
                                    loadedPackages.append(relatedPackage)
                                    if truck.getId() == 1:
                                        ht.setOnTruck(relatedPackage, time1)
                                        ht.setTruckId(relatedPackage, 1)
                                    if truck.getId() == 2:
                                        ht.setOnTruck(relatedPackage, time2)
                                        ht.setTruckId(relatedPackage, 2)
                    #if no special requirements for a package add it in sorted order
                    if package != 20 and package != 9 and package != 13 and package != 15 and package != 16 and package != 19 and package != 21 and package != 34 and package != 39 and package != 37 and package != 38 and package not in loadedPackages:
                        packagesToLoad.append(package)
                        loadedPackages.append(package)

                    #update the time on the hashtable object to indicate the time that the package has been loaded onto a truck, and which truck
                    if truck.getId() == 1:
                        ht.setOnTruck(package, time1)
                        ht.setTruckId(package, 1)
                    if truck.getId() == 2:
                        ht.setOnTruck(package, time2)
                        ht.setTruckId(package, 2)

    #load the truck
    truck.load(packagesToLoad)

#a function to find the distance between two points using their indexs corresponding to the location reference list
def getDistance(loc1, loc2):
    #use the index # loc 1 and loc 2 to get the address strings

    address1String = locReferenceList[loc1]
    address2String = locReferenceList[loc2]
    distance = 1000
    #check to make sure they are not the same address
    if address1String != address2String:
        #for each dictionary item check to see if it matches the address of either location
        for entry in distDict:
            if address1String in entry:
                list = distDict[entry]
                if len(list) > loc2 and (list[loc2] != 0) and (list[loc2] != 0.0):
                    distance = list[loc2]
            if address2String in entry:
                list = distDict[entry]
                if len(list) > loc1 and (list[loc1] != 0) and (list[loc1] != 0.0):
                    distance = list[loc1]
        return distance
    #if both location addresses are search and a non-zero value is not found, that means the distance is indeed 0
    else:
        distance = 0
        return distance

#a variable to track total miles traveled
totalMiles1 =0
totalMiles2 = 0
totalMilesAllTrucks = 0
#function for delivering the packages
def deliver(truck):


    #starting location is 0, the hub
    truckCurrentLocation = 0
    #get current inventory of the truck
    truckInventory = truck.getInventory()
    #while there are still packages in the truck
    isTruck1 = False
    global totalMiles1
    global totalMiles2
    global totalMilesAllTrucks

    while len(truckInventory) > 0:
        #get the package at index zero in the inventory
        package = truckInventory[0]
        #get the address of the package
        address = ht.retreiveAddress(package)
        #find the index of the address from the node reference list
        addressToDeliver = findNodeIndex(address)
        #get the distance from the current location to the address using the index
        distance = getDistance(truckCurrentLocation, addressToDeliver)
        #divide the distance by 18 since the trucks travel at 18 mph
        time = distance/18

        #if truck 1 set bool to true, add miles to next location to totalmiles1, elapse time1, and set the delivery time for the hash object
        if truck.getId() == 1:
            isTruck1 = True
            totalMiles1 =totalMiles1 + distance
            totalMilesAllTrucks = totalMilesAllTrucks + distance
            ht.setDeliveryMiles(truckInventory[0], totalMiles1)
            time1.elapseTime(time)
            #set the delivery time on the package object
            ht.setDelivery(package, time1)

        #same as above but for truck 2
        if truck.getId() == 2:
            isTruck1 = False
            totalMiles2 =totalMiles2 + distance
            totalMilesAllTrucks = totalMilesAllTrucks + distance
            ht.setDeliveryMiles(truckInventory[0], totalMiles2)
            time2.elapseTime(time)
            ht.setDelivery(package, time2)

        #set the currentlocation to the delivery address
        truckCurrentLocation = addressToDeliver
        #calls on deliver package in the truck class, which will remove the package from the trucks inventory
        truck.deliverPackage(package)
        #add the package to the delivered packages list
        deliveredPackages.append(package)

    #if packages still remain to be loaded return the truck to the hub and account for the distance
    if len(truckInventory) == 0:
        if (len(sortedPackages)) != (len(loadedPackages)):
            distanceBackToHub = getDistance(truckCurrentLocation, 0)
            if isTruck1:
                totalMiles1 += distanceBackToHub
                totalMilesAllTrucks += distanceBackToHub
            else:
                totalMiles2 += distanceBackToHub
                totalMilesAllTrucks += distanceBackToHub


#snapshot function takes a time and outputs the status of all packages at that time
def snapshot(time):
    milesTraveled1 = 0
    milesTraveled2 = 0
    deliveredPackagesSoFar = 0

    timeString = str(time)
    inputHour= 0
    inputMinute = 0

    #if the time input has 3 digits, ie 930, split into hours and minutes
    if len(timeString) == 3:
        inputHour = int(timeString[0:1])
        inputMinute = int(timeString[1:3])

    #if the time input has 4 digits, ie 1030, split into hours and minutes
    if len(timeString) == 4:
        inputHour = int(timeString[0:2])
        inputMinute = int(timeString[2:4])

    for package in deliveredPackages:
        #delivery time for package
        delivery = ht.retriveDelivery(package)

        #time the package was loaded onto the truck
        onTruck = ht.retreiveOnTruck(package)
        #the truck id that the package is on
        truckId = ht.retreiveTruckId(package)
        timeString = (str(time))
        #split the delivery time and time that the package was loaded onto the truck by the delimiter :
        deliverList = delivery.split(':')
        onTruckList = onTruck.split(':')
        #the hour will now be the first element in the list and minute will be the second
        onTruckHour = int(onTruckList[0])
        onTruckMinute = int(onTruckList[1])

        deliveryHour = int(deliverList[0])
        deliveryMinute = int(deliverList[1])

        #if package has been delivered according the the input hour
        if deliveryHour < inputHour:
            print("Delivered: package " + str(package) + " was delivered by truck " + str(truckId) + " at " + ht.retriveDelivery(package) + ".")
            #if truck1 and miles are largest than the current miles traveled, assign to the variable milesTraveled1, if truck2 assign the distance to milesTraveled2
            if ht.retreiveTruckId(package) == 1:
                if ht.retreiveDeliveryMiles(package) > milesTraveled1:
                    milesTraveled1 = ht.retreiveDeliveryMiles(package)
            if ht.retreiveTruckId(package) ==2:
                if ht.retreiveDeliveryMiles(package) > milesTraveled2:
                    milesTraveled2 = ht.retreiveDeliveryMiles(package)
            #add 1 onto the below variable since that package was delivered
            deliveredPackagesSoFar +=1

        #if delivery hour = input hour
        if deliveryHour == inputHour:
            if deliveryMinute <= inputMinute:
                print("Delivered: package " + str(package) + " was delivered by truck " + str(truckId) + " at " + ht.retriveDelivery(package) + ".")
                if ht.retreiveTruckId(package) ==1:
                    if ht.retreiveDeliveryMiles(package) > milesTraveled1:
                        milesTraveled1 = ht.retreiveDeliveryMiles(package)
                if ht.retreiveTruckId(package) ==2:
                    if ht.retreiveDeliveryMiles(package) > milesTraveled2:
                        milesTraveled2 = ht.retreiveDeliveryMiles(package)
                deliveredPackagesSoFar += 1
            #if the input minute is less than the delivery time the package hasnt yet been delivered
            if deliveryMinute > inputMinute:
                #if the time the package was loaded onto the truck equals the time inputted by the user, the package is loaded
                if onTruckHour == inputHour:
                    if onTruckMinute <= inputMinute:
                        print("Enroute: package " + str(package) + " was loaded onto truck " + str(truckId) + " at " + ht.retreiveOnTruck(package) + ".")
                    if onTruckMinute > inputMinute:
                        print("At the hub: Package " + str(package) + " has not yet been loaded onto a truck.")
                if onTruckHour < inputHour:
                    print("Enroute: package " + str(package) + " was loaded onto truck " + str(truckId) + " at " + ht.retreiveOnTruck(package) + ".")

        if deliveryHour > inputHour:
            if onTruckHour > inputHour:
                print("At the hub: Package " + str(package) + " has not yet been loaded onto a truck.")
            # if the input hour indicates the packages is not yet delivered but indicates that the package is loaded onto a truck via the input hour
            if onTruckHour < inputHour:
                print("Enroute: package " + str(package) + " was loaded onto truck " + str(truckId) + " at " + ht.retreiveOnTruck(package) + ".")
            # if the input hour indicates that the package is not yet delivered but indicates that the package is loaded onto a truck via the input minutes
            if onTruckHour == inputHour:
                if onTruckMinute <= inputMinute:
                    print("Enroute: package " + str(package) + " was loaded onto truck " + str(truckId) + " at " + ht.retreiveOnTruck(package) + ".")
                if onTruckMinute > inputMinute:
                    print("At the hub: Package " + str(package) + " has not yet been loaded onto a truck.")


    print(str(deliveredPackagesSoFar) + " packages have been delivered and " + str(milesTraveled1 + milesTraveled2) + " miles have been traveled.")


locationRefSimp()
computeRoute(0)
packageSort()

#load truck 1 and 2 in order to deliver the packages
while len(loadedPackages) < len(sortedPackages):
    load(truck1, time1)
    load(truck2, time2)

    deliver(truck1)
    deliver(truck2)

distanceList = []
totDist = 0
for i in range(len(deliveredPackages)):

    indexA = findNodeIndex(ht.retreiveAddress(deliveredPackages[i]))
    if (i+1) < len(deliveredPackages):
        indexB = findNodeIndex(ht.retreiveAddress(deliveredPackages[(i+1)]))
        distance = getDistance(indexA, indexB)
        distanceList.append(distance)
        totDist += distance

print(type(ht.retreiveTruckId(3)))

print("For package delivery status please type a 1 and press enter, for package data plese type a 2 and press enter.")
inputInitial = input("Please enter choice 1 or 2:")

if inputInitial == str(1):
    print("In order to look up the status of all packages at a specific time,")
    print("please enter a time using military standard, with no other characters.")
    input = input("Time: ")
    snapshot(input)

if inputInitial == str(2):
    for package in deliveredPackages:
        print(" ")
        print("Package " + str(package) + " data: ")
        print("     delivery address is  " + ht.retreiveFormattedAddress(package) + ",")
        print("     delivery deadline is " + ht.retreiveDeadline(package) + ",")
        if len(ht.retreiveNotes(package)) > 0:
            print("     delivery note is '" + str(ht.retreiveNotes(package)) + "',")
        print("     and package weight is " + ht.retreiveWeight(package) + " kg.")

print(" ")
print("A total of " + str(totalMilesAllTrucks) + " miles were traveled to deliver all packages.")

