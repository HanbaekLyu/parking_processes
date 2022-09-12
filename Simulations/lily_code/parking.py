import random as rnd
# import operator
# import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import math

class Line:

    def __init__(self, p, N):
        self.p = p # car density
        self.N = N # length of line
        self.CarList = []
        self.SpotList = []
        for position in range(self.N):
            x = rnd.random()
            if x <= self.p:
                car = Car(position)
                #print(position, 'car')
                self.CarList.append(car)
            else:
                self.SpotList.append(position)
                #print(position, 'spot')
        self.initCar = len(self.CarList)
        self.initSpot = len(self.SpotList)
        self.absorb = [0] * self.N
        #print(self.printLine())


    def update(self):
        # print(len(self.CarList), len(self.SpotList))
        for i in range(len(self.CarList)):
            car = self.CarList[i]
            x = rnd.random()
            if x <= 0.5:
                car.move(1) # +1
                if car.position == self.N:
                    car.setLocation(0)
            else:
                car.move(-1) # -1
                if car.position == -1:
                    car.setLocation(self.N-1)
        #print(self.printLine())
        self.coalesce()
        #print(self.printLine())
        self.park()
        #print(self.printLine())


    def coalesce(self):
        self.CarList.sort(key=lambda car: car.position)
        i = 0
        while i in range(len(self.CarList)-1):
            if len(self.CarList) == 1:
                break
            elif self.CarList[i].position == self.CarList[i+1].position:
                self.CarList[i].PassengerList.extend(self.CarList[i+1].PassengerList)
                self.CarList.pop(i+1)
            else:
                i += 1


    def park(self):
        self.CarList.sort(key=lambda car: car.position)
        # self.SpotList.sort()
        i = 0
        while i in range(len(self.SpotList)):
            j = 0
            while j in range(len(self.CarList)):
                if self.CarList[j].position == self.SpotList[i]:
                    self.absorb[self.SpotList[i]] = self.CarList[j].count()
                    self.CarList.pop(j)
                    self.SpotList.pop(i)
                    if i >= len(self.SpotList):
                        break
                else:
                    j += 1
            i += 1


    def continueProgram(self):
        if len(self.SpotList) == 0:
            return False
        elif len(self.CarList) == 0:
            return False
        else:
            return True


    def numOfParticles(self):
        return [len(self.CarList), len(self.SpotList)]


    def initilization(self):
        return [self.initCar, self.initSpot]


    def gamma(self):
        if self.initSpot != 0:
            return sum(self.absorb)/self.initSpot
        else:
            return 0

    def printLine(self):
        L = [0] * self.N
        for i in range(len(self.CarList)):
            pos = self.CarList[i].position
            pasL = self.CarList[i].PassengerList
            L[pos] = pasL
        return L


class Car:

    def __init__(self, position):
        self.position = position
        self.PassengerList = []
        self.PassengerList.append(position)

    def move(self, x):
        self.position += x

    def setLocation(self, x):
        self.position = x

    def count(self):
        return len(self.PassengerList)



def findpc(N, trial):
    carLeft = []
    spotLeft = []
    gammaList = []
    for x in range(50, 81, 1):
        p = x / 100
        print(p)
        car = 0
        spot = 0
        gamma = 0
        for i in range(trial):
            print(i)
            line = Line(p, N)
            initCar = line.initilization()[0]
            initSpot = line.initilization()[1]
            # print(line.initilization())
            while line.continueProgram():
                line.update()
            # print(line.numOfParticles())
            # print(line.gamma())
            car += line.numOfParticles()[0] / initCar
            spot += line.numOfParticles()[1] / initSpot
            gamma += line.gamma()
        carLeft.append(car / trial)
        spotLeft.append(spot / trial)
        gammaList.append(gamma / trial)

    xaxis = np.arange(0.5, 0.8, 0.01)

    plt.figure(1)
    plt.xlabel('p')
    plt.ylabel('Avg num of cars left')
    plt.plot(xaxis, carLeft)

    plt.figure(2)
    plt.xlabel('p')
    plt.ylabel('Avg num of spots left')
    plt.plot(xaxis, spotLeft)

    plt.figure(3)
    plt.xlabel('p')
    plt.ylabel('Gamma')
    plt.plot(xaxis, gammaList)

    plt.show()


def timeElapse(p, N, trial):
    dataCar = [0] * 1000000
    #dataSpot = [0] * 1000000
    #dataRatio = [0] * 1000000
    jList = [0] * trial
    for i in range(trial):
        line = Line(p, N)
        print(line.initilization())
        initCar = line.initilization()[0]
        #initSpot = line.initilization()[1]
        tempCar = [0] * len(dataCar)
        #tempSpot = [0] * len(dataSpot)
        #tempRatio = [0] * len(dataRatio)
        # tempCar[0] = 1
        #tempSpot[0] = 1
        #tempRatio[0] = initSpot / initCar
        j = 0
        while line.continueProgram():
            j += 1
            line.update()
            # print(line.numOfParticles())
            [curCar, curSpot] = line.numOfParticles()
            # print(curCar/initCar, curSpot/initSpot)
            tempCar[j] = math.sqrt(j) * curCar / initCar
            #tempSpot[j] = curSpot / initSpot
            #if curCar != 0:
                #tempRatio[j] = curSpot / curCar
        print(line.numOfParticles())
        jList[i] = j
        # print(j)
        # print(tempCar[j])
        for x in range(j + 1, 1000000):
            tempCar[x] = tempCar[j] * math.sqrt(x) / math.sqrt(j)
            #tempSpot[x] = tempSpot[j]
            #tempRatio[x] = tempRatio[j]
        # print(tempCar)
        for x in range(1000000):
            dataCar[x] += tempCar[x]
            #dataSpot[x] += tempSpot[x]
            #dataRatio[x] += tempRatio[x]
        # print(dataCar)
        # print(dataSpot)
        # print(dataRatio)
    j = max(jList)
    print(j)
    car = [x / trial for x in dataCar]
    car = car[:j + 1]
    #spot = [x / trial for x in dataSpot]
    #spot = spot[:j + 1]
    #ratio = [x / trial for x in dataRatio]
    #ratio = ratio[:j + 1]
    # print(car)
    # print(spot)
    # print(ratio)

    xaxis = np.arange(j + 1)
    plt.figure(1)
    plt.xlabel('t')
    plt.ylabel('car')
    plt.plot(xaxis, car)

    #plt.figure(2)
    #plt.xlabel('t')
    #plt.ylabel('spot')
    #plt.plot(xaxis, spot)

    #plt.figure(3)
    #plt.xlabel('t')
    #plt.ylabel('ratio')
    #plt.plot(xaxis, ratio)

    plt.show()


def test(p, N):
    line = Line(p, N)
    while line.continueProgram():
        line.update()


# findpc(1000, 100)
#timeElapse(0.75, 500, 500)

#test(0.75, 20)