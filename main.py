from lib import Session
from time import sleep, time
from pprint import pprint

LOGIN, PASSWORD = "FancyPotatoFoodZProszku", "Proszek"
e = 0.001
EXPECTED_LATENCY=.3


def main(data, move, jump, stop, rocket, blackhole):
    
    def has_same_Y(p):
        return abs(p["Y"] - data['myStats']['Y']) < e

    my_platform = list(filter(has_same_Y, data['platforms']))
    if len(my_platform) > 1:
        print("Found more of them !!")
    elif len(my_platform) == 0:
        rocket(0, -1, 0, 0.001)
        return

    my_platform = my_platform[0]
    
    target_platform = my_platform

    distance_x, distance_z = target_platform["X"]-data['myStats']['X'], target_platform['Z']-data['myStats']['Z']
    distance = (distance_x**2 + distance_z**2)**.5

    force_jump = False;
    if distance/5 < EXPECTED_LATENCY/2: move(distance_x, distance_z)
    else:
        stop()
        if abs(my_platform['Radius']-distance)/.5 < EXPECTED_LATENCY:
            force_jump = True

    if force_jump or my_platform['Radius']/.5 < 2*EXPECTED_LATENCY:
        jump()
        rocket(0, -1, 0, 0.001)


s = Session(LOGIN, PASSWORD, main)

TPS = 60
TICK_LEN = 1/TPS
while True:
    last_time = time()
    s.tick()
    took = time() - last_time
    print("Tick took %fs" % took, end="\r")
    if took < TICK_LEN: sleep(TICK_LEN - took)
    
