class Vehicle(object):
    def __init__(self, make):
        self.make = make
    pass

class Wheeled(Vehicle):
    def __init__(self, make, wheels):
        self.wheels = wheels
        Vehicle.__init__(self, make)
    
    def getNumOfWheels(self):
        return self.wheels
    pass

class Motorised(Wheeled):
    def __init__(self, make, wheels, typeOfEngine):
        self.typeOfEngine = typeOfEngine
        Wheeled.__init__(self, make, wheels)
    
    def switchOn(self):
        print("Motor is on")
    pass

class Aircraft(Motorised):
    def __init__(self, make, wheels, typeOfEngine):
        Motorised.__init__(self, make, wheels, typeOfEngine)
    
    def takeOff(self):
        print(self.make, self.wheels, self.typeOfEngine)
    pass

aPlane = Aircraft("Boeing", 3, "kerosene")
aPlane.switchOn()
aPlane.takeOff()
