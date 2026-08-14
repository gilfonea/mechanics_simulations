#main.py

from vpython import *
from models.two_bodies_on_incline import Two_bodies_on_incline

def main():

   
    sim = Two_bodies_on_incline()
    sim.start()

    while True:
        pass


if __name__ == "__main__":
    main()