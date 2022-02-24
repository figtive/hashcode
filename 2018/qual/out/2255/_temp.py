import sys
import time

TESTCASE = sys.argv[1]
DEBUG = False


def main():
    row_c, col_c, vehicle_c, ride_c, bonus, step_c = sys.stdin.readline().strip().split(" ")
    row_c, col_c, vehicle_c, ride_c, bonus, step_c = int(row_c), int(col_c), int(vehicle_c), int(ride_c), int(bonus), int(step_c)
    if DEBUG:
        print("CONFIG")
        print(f"Rows:{row_c} Column:{col_c} Vehicles:{vehicle_c} Rides:{ride_c} Bonus:{bonus} Steps:{step_c}\n")
    rides = []
    for i in range(ride_c):
        from_r, from_c, to_r, to_c, start, finish = sys.stdin.readline().strip().split(" ")
        rides.append(Ride(i, (int(from_r), int(from_c)), (int(to_r), int(to_c)), int(start), int(finish)))
    if DEBUG:
        print("RIDES")
        print(f"Rows:{row_c} Column:{col_c} Vehicles:{vehicle_c} Rides:{ride_c} Bonus:{bonus} Steps:{step_c}")
        for ride in rides:
            print(ride)
        print("")

    # TODO: sort
    rides.sort(key=lambda r: (r.st, r.fi))

    if DEBUG:
        print("Sorted rides")
        for ride in rides:
            print(ride)
        print("")

    # init vehicles
    vehicles = []
    for i in range(vehicle_c):
        vehicles.append(Vehicle(i))

    for step in range(step_c):
        if step_c // 20 and not step % (step_c // 20):
            log(f"{step / step_c * 100:.1f}%")
        for v in vehicles:
            if v.state == Vehicle.DELIVERING:
                v.step()
            elif v.state == Vehicle.OTW:
                v.step()
            elif v.state == Vehicle.WAITING:
                if step == v.ride.st:
                    v.state = Vehicle.DELIVERING
                    v.step()
            if v.state == Vehicle.IDLE:
                def d_to_start(r, v):
                    return abs(r.f[1] - v.pos[1]) + abs(r.f[0] - v.pos[0])
                # if not len(rides):
                #     continue
                # rides = sorted(lambda r: (r.st, d_to_start(r, v), r.d, r.fi - (step + d_to_start(r, v) + r.d)), frides)
                # frides.sort(key=lambda r: (r.st, r.d))
                frides = list(filter(lambda r: step + d_to_start(r, v) + r.d < r.fi and r.st <= step, rides))
                if not len(frides):
                    continue
                frides.sort(key=lambda r: (r.st, d_to_start(r, v), r.d, r.fi - (step + d_to_start(r, v) + r.d)))
                v.assign_ride(frides.pop(0))
                # if v.ride in rides: rides.remove(v.ride)
                rides.remove(v.ride)
                if d_to_start(v.ride, v) == 0 and step == v.ride.st:
                    v.state = Vehicle.DELIVERING
                    if not step:
                        v.step()
                elif d_to_start(v.ride, v) == 0 and step < v.ride.st:
                    v.state = Vehicle.WAITING
                else:
                    v.state = Vehicle.OTW
                    if not step:
                        v.step()
                '''
                1. start at same position
                2. by earlier start
                3. by longest distance
                '''
    # print("SOLUTION")
    for v in vehicles:
        print(f"{len(v.history)} {' '.join([str(r.id) for r in v.history])}", file=sys.stderr)

    # print("\nSCORE")
    # print(f"{calc_score(vehicles, bonus, calc_c):,}")
    
    
def calc_score(vehicles, bonus, step_c):
    score = 0
    for v in vehicles:
        step = 0
        pos = [0, 0]        
        for step in range(step_c):
            pass
        for r in v.history:
            score += abs(r.t[1] - r.f[1]) + abs(r.t[0] - r.f[0])
            if r.f[0] != pos[0] or r.f[1] != pos[1]:
                step += abs(r.f[1] - pos[1]) + abs(r.f[0] - pos[0])
                pos = list(r.f)
            if (r.f[0] == pos[0] and r.f[1] == pos[1] and r.st == step) or (step + abs(r.f[1] - pos[1]) + abs(r.f[0] - pos[0]) == r.st):
                score += bonus
            step += abs(r.t[1] - pos[1]) + abs(r.t[0] - pos[0])
            pos = list(r.t)
    return score


class Ride:
    def __init__(self, _id, f, t, start, finish):
        self.id = _id
        self.f = f
        self.t = t
        self.st = start
        self.fi = finish
        self.d = abs(t[1] - f[1]) + abs(t[0] - f[0])
        self.taken = False

    def __str__(self):
        return f"From:{self.f[0]},{self.f[1]} To:{self.t[0]},{self.t[1]} Start:{self.st} Finish:{self.fi}"
        
    def __repr__(self):
        return str(self)

class Vehicle:
    IDLE, OTW, WAITING, DELIVERING = range(4)
    def __init__(self, _id):
        self.id = _id
        self.pos = [0, 0]

        self.state = self.IDLE
        self.ride = None

        self.history = []

    def step(self):
        if self.state == self.DELIVERING or self.state == self.OTW:
            self.ride.d -= 1
            if self.ride.d == 0:
                self.pos = list(self.ride.t)
                self.state = self.IDLE
    
    def assign_ride(self, ride):
        self.ride = ride
        self.history.append(ride)

def log(message):
    print(f"{TESTCASE:12.12}\t{message}")

if __name__ == "__main__":
    start = time.perf_counter()
    log("------------------------ START")
    main()
    log(f"------------------------ FINISH @ {time.perf_counter() - start:.6f}s")
