import random

class Car:
    def __init__(self, name, vin_number, model):
        self.name = name
        self.vin_number = vin_number
        self.model = model
    
    def __str__(self):
        return f"Name: {self.name}  Vin:{self.vin_number}  Model: {self.model}"

class Human:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.current_car = None
        self.cars = None

    def getName(self):
        return self.name

    def getCurrentCar(self):
        if(self.current_car != None):
            return self.current_car
        else:
            print("No current car")
    
    def setCurrentCar(self, id):
        try:
            self.current_car = self.cars[id]
        except IndexError:
            print("Incorrect index")

    def setCars(self, cars):
        self.cars = cars
    
    def getCars(self):
        return self.cars

    def showCars(self):
        print(f"{self.name}`s cars:")
        if(self.cars != None):
            for i in range(len(self.cars)):
                print(f"\t{i}: {self.cars[i]}\n")
        else:
            print("\tNo cars")
        
    def showCarsInformation(self):
        self.showCars()
        if(self.current_car != None):
            print(f"\tCurrent car: {self.current_car}")
        else:
            print("\tNo current car")




human1 = Human("Victor", 25)
human2 = Human("Mike", 52)

models = ["Mercedes Benz", "Audi", "BMW", "Honda"]

names = ["W8", "Sport", "Camry", "X1", "Taigun", "Turbo AT",
         "Fortuner", "Sonet", "Land Cruiser", "Nexo"]

cars = list()

for i in range(10):
    cars.append(Car(names[i], str(random.randint(1000000, 9999999)), models[random.randint(0, 3)]))

human1.setCars(cars[0:5])
human2.setCars(cars[5:10])

human1.showCarsInformation()
human2.showCarsInformation()

print("\n")

try:
    carId1 = int(input(f"Choose which car {human1.getName()} will ride today by ID: "))
    human1.setCurrentCar(carId1)
except:
    print("Incorrect index")

try:
    carId2 = int(input(f"Choose which car {human2.getName()} will ride today by ID: "))
    human2.setCurrentCar(carId2)
except:
    print("Incorrect index")

print("\n")

human1.showCarsInformation()
human2.showCarsInformation()

input()
