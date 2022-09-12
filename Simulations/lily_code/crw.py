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
        for position in range(self.N):
            x = rnd.random()
            if x <= self.p:
                car = Car(position)
                #print(position, 'car')
                self.CarList.append(car)
        self.initCar = len(self.CarList)


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

    """
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
    """

    def continueProgram(self):
        if len(self.CarList) == 2:
            return False
        else:
            return True


    def numOfParticles(self):
        return len(self.CarList)


    def initilization(self):
        return self.initCar

    """
    def gamma(self):
        if self.initSpot != 0:
            return sum(self.absorb)/self.initSpot
        else:
            return 0
    """

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

def timeElapse(p, N, trial):
    dataCar = [0] * 1000000
    jList = [0] * trial
    for i in range(trial):
        print(i)
        line = Line(p, N)
        # print(line.initilization())
        initCar = line.initilization()
        tempCar = [0] * len(dataCar)
        j = 0
        while line.continueProgram():
            j += 1
            line.update()
            # print(line.numOfParticles())
            curCar = line.numOfParticles()
            # print(curCar/initCar, curSpot/initSpot)
            tempCar[j] = math.sqrt(j) * curCar / initCar
        # print(line.numOfParticles())
        jList[i] = j
        # print(j)
        # print(tempCar[j])
        for x in range(j + 1, 1000000):
            tempCar[x] = tempCar[j] * math.sqrt(x) / math.sqrt(j)
        # print(tempCar)
        for x in range(1000000):
            dataCar[x] += tempCar[x]
        # print(dataCar)
    #j = max(jList)
    #print(j)
    car = [x / trial for x in dataCar]
    #car = car[:j + 1]
    # print(car)

    xaxis = np.arange(1000000)
    plt.figure(1)
    plt.xlabel('t')
    plt.ylabel('car')
    plt.plot(xaxis, car)

    plt.show()

timeElapse(0.75, 500, 500)