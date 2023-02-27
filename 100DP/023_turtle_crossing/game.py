"""Controls all the settings from the game related to the cars and difficulty"""
import random as r
import car


class Game:

    def __init__(self):
        self.lanes = [n for n in range(-200, 220, 40)]
        self.starting_pos = 350
        self.cars_moving = []
        self.cars_parked = []
        self.iterations = 20
        self.time = 0.1

    def next_level(self):
        """Moves on to te next level, increasing difficulty"""
        if self.iterations > 4:
            self.iterations -= 1
        if self.time > 0.05:
            self.time -= 0.005
        for c in self.cars_moving:
            self.park_car_internal(c)
        self.cars_moving.clear()

    def start_car(self):
        """Start a car from the beginning, either a parked car or a new car"""
        if len(self.cars_parked):
            self.cars_moving.append(self.cars_parked.pop())
        else:
            self.cars_moving.append(car.Car((self.starting_pos, r.choice(self.lanes))))

    def park_car(self, cur_car):
        """Park a car, so we can use it later when needed"""
        self.cars_moving.remove(cur_car)
        self.park_car_internal(cur_car)

    def park_car_internal(self, cur_car):
        """Repeated functionality to park a car"""
        cur_car.park_car((self.starting_pos, r.choice(self.lanes)))
        self.cars_parked.append(cur_car)
