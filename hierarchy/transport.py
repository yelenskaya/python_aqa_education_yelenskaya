"""
OOP hierarchy task

Use of abstract classes, methods, inheritance, multiple inheritance,
overriding methods, magic methods,
using @classmethod, @staticmethod, @property decorators
"""
from abc import ABC, abstractmethod


class Transport(ABC):
    """
    Describes basic transport
    """
    REGISTERED_VEHICLES = []

    def __init__(self, name, capacity, max_speed):
        self.name = name
        self.capacity = capacity
        self.max_speed = max_speed
        self._current_speed = None

    def __rshift__(self, destination):
        print(f"Destination is {destination}")

    def __lshift__(self, last_destination):
        print(f"Returning from {last_destination}")

    @abstractmethod
    def travel(self):
        """
        Describes traveling logic
        """
        ...

    @property
    def current_speed(self):
        """
        Get current speed
        :return:
        """
        return self._current_speed

    @current_speed.setter
    def current_speed(self, target_speed):
        if target_speed <= self.max_speed:
            self._current_speed = target_speed
            print(f"Changing speed to {target_speed} km per hour")
        else:
            self._current_speed = self.max_speed
            print(f"The vehicle can speed up only to {self.max_speed} km per hour")

    @classmethod
    def register_vehicle(cls, vehicle):
        """
        Add a vehicle to registered vehicles list
        """
        cls.REGISTERED_VEHICLES.append(vehicle.name)


class CargoVehicle(ABC):
    """
    Describes a basic cargo vehicle
    """
    def __init__(self, hold=None):
        if hold is None:
            hold = []
        self.hold = hold

    def __add__(self, cargo):
        print(f"Loading {cargo}")
        self.hold.append(cargo)

    def __sub__(self, cargo):
        print(f"Offloading {cargo}")
        if cargo in self.hold:
            self.hold.remove(cargo)
        else:
            print(f"We do not have {cargo}")

    def __contains__(self, item):
        is_present = item in self.hold
        print(f"{item} is {'' if is_present else 'not '}in hold")
        return item in self.hold

    def deliver(self):
        """
        Deliver all cargo in hold
        """
        print(f"Delivering cargo in hold: {self.hold}")


class Ship(Transport):
    """
    Describes water-floating vehicles
    """

    def __init__(self, name, capacity, max_speed, draft):
        super().__init__(name, capacity, max_speed)
        self.draft = draft

    def __invert__(self):
        print("Launch the ship")

    def travel(self):
        """
        Describes ship traveling
        """
        print("Travel by sea")

    @staticmethod
    def listen_to_sea_shanty():
        """
        Listen to sea shanty
        """
        print("""=========================
Soon may the Wellerman come
To bring us sugar and tea and rum
=========================""")


class Truck(Transport):
    """
    Describes truck vehicles
    """
    def __init__(self, name, capacity, max_speed, body_type):
        super().__init__(name, capacity, max_speed)
        self.body_type = body_type

    def travel(self):
        """
        Describes truck traveling
        """
        print("Travel by road")


class Train(Transport):
    """
    Describes train vehicles
    """
    def __init__(self, name, capacity, max_speed, number_of_cars):
        super().__init__(name, capacity, max_speed)
        self.number_of_cars = number_of_cars

    def travel(self):
        """
        Describes train traveling
        """
        print("Travel by railroad")


class Aircraft(Transport):
    """
    Describes aircraft vehicles
    """

    def __init__(self, name, capacity, max_speed, max_cruising_altitude):
        super().__init__(name, capacity, max_speed)
        self.max_cruising_altitude = max_cruising_altitude

    def travel(self):
        """
        Describes aircraft traveling
        """
        print("Travel by air")


class CargoShip(Ship, CargoVehicle):
    """
    Describes cargo ship
    """
    def __init__(self, name, capacity, max_speed, draft):
        Ship.__init__(self, name, capacity, max_speed, draft)
        CargoVehicle.__init__(self)

    def deliver(self):
        """
        Travel as ship, delivering all in hold
        """
        self.travel()
        CargoVehicle.deliver(self)


cargo_ship = CargoShip("Bananana", 5000, 45, 12.04)
other_ship = Ship("Official ship name", 6000, 45, 12.04)

Transport.register_vehicle(other_ship)
Transport.register_vehicle(cargo_ship)
print(Transport.REGISTERED_VEHICLES)

cargo_ship + "Elephant"
cargo_ship + "Penguin"
cargo_ship + "Zebra"
cargo_ship - "Zebra"
cargo_ship - "Monkey"
"Elephant" in cargo_ship
"Tiger" in cargo_ship
~cargo_ship
cargo_ship >> "Madagascar"
cargo_ship.deliver()

cargo_ship.current_speed = 20
cargo_ship.current_speed = 55

CargoShip.listen_to_sea_shanty()

cargo_ship << "Madagascar"
