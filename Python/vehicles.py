#Proactive Analytics technical assignment
#Question1

class Vehicle(object):
    ''' Base Class in the vehicle hierachy'''
    def __init__(self, make):
        self.make = make
    pass

#Added default values for parameters to avoid constructor errors
class Wheeled(Vehicle):
    def __init__(self, make, wheels = 2):
        self.wheels = wheels
        Vehicle.__init__(self, make)
    
    def getNumOfWheels(self):
        return self.wheels
    pass

class Motorised(Wheeled):
    def __init__(self, make, wheels, typeOfEngine = "diesel"):
        self.typeOfEngine = typeOfEngine
        Wheeled.__init__(self, make, wheels)
    
    def switchOn(self):
        print("Motor is on")
    pass

class Aircraft(Motorised):
    def __init__(self, make, wheels, typeOfEngine):
        Motorised.__init__(self, make, wheels, typeOfEngine)
    
    def takeOff(self):
        output = ("Airplane make: {} \nNum of wheels: {} \nType of Engine: {}"
                  .format(self.make, self.wheels, self.typeOfEngine))
        print(output)
    pass

