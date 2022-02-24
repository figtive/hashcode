import sys
import time as tt
from itertools import cycle
import random

TESTCASE = sys.argv[1] if len(sys.argv) > 1 else ""
DEBUG = False

def main():
    # PARSE
    D, intersection_c, street_c, car_c, F = sys.stdin.readline().strip().split(" ")
    D, intersection_c, street_c, car_c, F = int(D), int(intersection_c), int(street_c), int(car_c), int(F)
    intersections = []
    streets = {}
    cars = []
    streets_popularity = {}
    start_streets_popularity = {}
    intersection_popularity = []
    intersection_street_length = []
    for i in range(intersection_c):
        intersections.append(Intersection(i))
        intersection_popularity.append(0)
        intersection_street_length.append(0)
    for _ in range(street_c):
        start, end, name, L = sys.stdin.readline().strip().split(" ")
        start, end, name, L = int(start), int(end), name, int(D) 
        street = Street(name, intersections[start], intersections[end], L)
        streets[name] = street
        intersections[end].streets_in.append(street)
        intersections[start].streets_out.append(street)
        streets_popularity[name] = 0
        start_streets_popularity[name] = 0
        intersection_street_length[end] += L
    for i in range(car_c):
        _, *routes = sys.stdin.readline().strip().split(" ")
        street_obj = []
        for j, street in enumerate(routes):
            streets_popularity[street] += 1
            intersection_popularity[streets[street].end.id] += 1
            street_obj.append(streets[street])
            if j == 0:
                start_streets_popularity[street] += 1
        cars.append(Car(i, street_obj))
    if DEBUG:
        log("\nINTERSECTIONS")
        for intersection in intersections:
            log(intersections)
        log("\nSTREETS")
        for street in streets.values():
            log(street)
        log("\nCARS")
        for car in cars:
            log(car)

    '''
    - unused street -> always red
    - intersection w/ only 1 in -> always green
    - schedule must loop a few times in single run to avoid car getting stuck
    - schedule is relative to simulation length, other street popularity, street count
    '''

    # TODO: sort?
    
    # CREATE SCHEDULE
    for intersection in intersections:
        schedule = []  # [(street_name, duration)]
        for street in intersection.streets_in:
            if streets_popularity[street.name] > 0 or intersection_popularity[intersection.id] > 0:
                # TODO find a good way to decide how many should the schedule be looped
                constant = 2 if D < 10 else 1000
                duration = streets_popularity[street.name] * ((street.L / intersection_street_length[intersection.id])) / intersection_popularity[intersection.id] * D // constant
                if duration == 0:
                    duration = 1
                schedule.append((street.name, duration))
        schedule.sort(key=lambda s: start_streets_popularity[s[0]], reverse=True)
        intersection.set_schedule(schedule)
    
    # SOLUTION
    sintersections = [i for i in intersections if len(i.schedule)]
    print(len(sintersections), file=sys.stderr)
    for intersection in sintersections:
        print(intersection.id, file=sys.stderr)
        print(len(intersection.schedule), file=sys.stderr)
        for name, duration in intersection.schedule:
            print(f"{name} {duration:.0f}", file=sys.stderr)
    
    # MAIN SIMULATION LOOP
    score = 0
    for T in range(D):
        '''
        1. step intersection lights
        2. step car
        '''
        for i in intersections:
            i.step(T)
        for c in cars:
            score += c.step(T, D, F)
    
    # SCORE
    print(f"SCORE: {score}")


def log(message, force=False):
    if DEBUG or force:
        print(f"{TESTCASE:12.12}\t{message}")


class Car:
    def __init__(self, _id, streets):
        self.id = _id
        self.streets = streets
        self.streets_hop = streets[1::]
        self.current_street = streets[0]
        self.current_street.cars.insert(0, self)
        self.Lremaining = 0
     
    def step(self, T, D, F):
        if self.Lremaining == 0:
            if self.current_street.cars[-1] != self:
                return 0 # wait until turn to hop
            # hop intersection
            if self.current_street.end.green[0] == self.current_street.name:
                self.current_street.cars.pop()
                self.current_street = self.streets_hop.pop(0)
                self.Lremaining = self.current_street.L # @intersection, move INTO next street @next step
            if len(self.streets_hop) != 0:
                # hop to new street
                self.current_street.cars.insert(0, self)
                return 0
            else:
                # end of journey
                print("END", D, T, D-T)
                return F + (D - T) if (D - T) >= 0 else 0
        else:
            # reduce L
            self.Lremaining -= 1
            return 0
    
    def __str__(self):
        return f"{self.id} {self.streets}"


class Intersection:
    def __init__(self, _id):
        self.id = _id
        self.streets_in = []
        self.streets_out = []
        self.schedule = [] # (street-name, greenduration)
        self.schedule_cycle = None
        self.green = ["", 0] # [streetname,untilred]

    def set_schedule(self, schedule):
        self.schedule = schedule
        self.schedule_cycle = cycle(self.schedule)
        self.dead = len(schedule) == 0
        if not self.dead:
            self.green = list(next(self.schedule_cycle))

    def step(self, T):
        if self.dead:
            return
        if self.green[1] == 0:
            self.green = list(next(self.schedule_cycle))
        self.green[1] -= 1

    def __str__(self):
        return f"{self.id} st_in:{self.streets_in} st_out:{self.streets_out} green:{self.green}"

    def __repr__(self):
        return str(self)


class Street:
    def __init__(self, name, start, end, L):
        self.name = name
        self.start = start
        self.end = end
        self.cars = []
        self.L = L
    
    def __str__(self):
        return f"{self.name} start:{self.start.id} end:{self.end.id} L:{self.L}"

    def __repr__(self):
        return str(self)


if __name__ == "__main__":
    start = tt.perf_counter()
    log("------------------------ START", True)
    main()
    log(f"------------------------ FINISH @ {tt.perf_counter() - start:.6f}s", True)
