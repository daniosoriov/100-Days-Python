"""This module creates a simulation of a coffe machine"""
MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}


def print_report(res):
    """Prints the resources"""
    print(f'Water: {res["water"]}ml')
    print(f'Milk: {res["milk"]}ml')
    print(f'Coffee: {res["coffee"]}g')
    # Initialize money.
    res['money'] = res.get('money', 0)
    print(f'Money: ${res["money"]}')


def check_resources(menu, drink, res):
    """Checks if there are enough resources for the desired drink.
    Returns True if there are enough resources. False otherwise"""
    # checks = (False for k, v in menu[drink]['ingredients'].items() if v > res[k])
    checks = []
    for key, val in menu[drink]['ingredients'].items():
        if val > res[key]:
            print(f'  Sorry, there is not enough {key}.')
            checks.append(False)
    return False not in checks


def update_resources(menu, drink, res):
    """Update the resources with the values of usage from the selected drink on the menu"""
    # If money isn't there, initialize it.
    res['money'] = res.get('money', 0) + menu[drink]['cost']
    for key, val in menu[drink]['ingredients'].items():
        res[key] -= val
    return res


def get_money():
    """Prompts the user to input the coins and returns the sum of the money"""


    def get_valid_integer(text):
        """Prompts a question undefinitely until the answer is a valid int"""
        while True:
            try:
                val = int(input(text))
                return val
            except ValueError:
                print('Please enter a valid integer.')


    quarters = get_valid_integer('How many quarters?: ') * 0.25
    dimes = get_valid_integer('How many dimes?: ') * 0.10
    nickels = get_valid_integer('How many nickels?: ') * 0.05
    pennies = get_valid_integer('How many pennies?: ') * 0.01
    return round(quarters + dimes + nickels + pennies, 2)


# Actual loop
while True:
    option = input('  What would you like? (espresso/latte/cappuccino): ')
    while option not in ('espresso', 'latte', 'cappuccino', 'off', 'report'):
        option = input('Please only type espresso, latte or cappuccino: ')
    if option == 'off':
        print('Turning the machine off.')
        break
    if option == 'report':
        print_report(resources)
        continue
    if check_resources(MENU, option, resources):
        cost = MENU[option]['cost']
        print(f'Your {option} costs ${cost}.')
        print('Please insert coins.')
        money = get_money()
        print(f'You inserted ${money}.')
        if money < cost:
            print('Sorry that\'s not enough money. Money refunded.')
        else:
            rest = round(money - cost, 2)
            print(f'Here is ${rest} (${money} - ${cost}) dollars in change.')
            print(f'Here is your {option}: ☕️. Enjoy!')
            resources = update_resources(MENU, option, resources)

print('Goodbye!')
