"""
Creator: Sonja Ek
Created: 15.3.2020
This is a text-based driving simulator. We have a car that requires 
regular gas fill-ups. After each time we move the car the program will
tell us the current coordinates and the amount of gas we have left.
"""

from math import sqrt

# First things first: How much gas can we have?
def main():
    tank_size = read_number("How much does the vehicle's gas tank hold? ")
    gas = tank_size  # Tank is full when we start
    gas_consumption = read_number("How many liters of gas does the car " +
                                  "consume per hundred kilometers? ")
    x = 0.0  # Current X coordinate of the car
    y = 0.0  # Current Y coordinate of the car

    while True:
        print("Coordinates x={:.1f}, y={:.1f}, "
              "the tank contains {:.1f} liters of gas.".format(x, y, gas))

        choice = input("1) Fill 2) Drive 3) Quit\n-> ")

        # The user wants to fill up the tank. Let's ask how many liters to use 
        # and see how full the tank gets:
        if choice == "1":
            to_fill = read_number("How many liters of gas to fill up? ")
            gas = fill(tank_size, to_fill, gas)

        # The user wants to drive. Let's see where the car ends up:
        elif choice == "2":
            target_x = read_number("x: ")
            target_y = read_number("y: ")
            gas, x, y = drive(x, y, target_x, target_y, gas, gas_consumption)
        elif choice == "3":
            break
            
    print("Thank you and bye!")


def fill(tank_size, to_fill, gas):
    # The amount of gas the user wants to use fits in the tank:
    if (gas + to_fill) > tank_size:
        gas = tank_size
    # Not all the gas fits in the tank, we need to leave out
    # the excess amount:
    else:
        gas = gas + to_fill
    # The amount of gas the car has after adding:
    return gas


def drive(x, y, target_x, target_y, gas, gas_consumption):
    new_x = target_x - x
    new_y = target_y - y
    # We're gonna need a function called distance to calculate 
    # the distance between the old and the new locations:
    dist = distance(new_x, new_y)

    # We're only letting the car move if there's enough gas.
    # Below we have a function called enough_gas to check that.
    if enough_gas(gas, gas_consumption, dist):
        x = x + new_x
        y = y + new_y
        gas = new_gas(gas, gas_consumption, new_x, new_y)

        return gas, x, y
    else:
        x = x + (100 * gas / gas_consumption) / dist * new_x
        y = y + (100 * gas / gas_consumption) / dist * new_y
        return 0, x, y

    
# This function calculates the distance between the old and new locations
# using the Pythagorean theorem:
def distance(new_x, new_y):
    linnuntie = sqrt(new_x ** 2 + new_y ** 2)
    return linnuntie


# This function checks whether we have enough gas to drive to the 
# proposed location:
def enough_gas(gas, gas_consumption, dist):
    if gas < gas_consumption * dist / 100:
        return False
    else:
        return True

# This function checks the amount of gas left after driving based
# on the travelled distance and gas consumption:
def new_gas(gas, gas_consumption, new_x, new_y):
    gas = gas - gas_consumption * sqrt(new_x ** 2 + new_y ** 2) / 100
    return gas

# This function checks the validity of the user's (x,y) location input:
def read_number(prompt, error_message="Incorrect input!"):
    try:
        return float(input(prompt))
    except ValueError:
        print(error_message)
        return read_number(prompt, error_message)


main()   