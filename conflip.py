# importing the random module lets us use the random.choice function
import random

# this defines a simple function that needs no input
def flipCoin():
    return random.choice(['heads', 'tails'])

# this function needs two inputs
def guessed_right(coin, guess):
    if ( coin == guess ):
        return True
    else:
        return False

# This function needs one input
def notify_of_outcome(status):
    if status == True:
        print("You won!")
    else:
        print("You have failed at everything.")

def run_game():
    coin = flipCoin()
    #print(coin)
    guess = input("heads/tails: ")
    notify_of_outcome(guessed_right(coin, guess))

for i in range(0,5):
    run_game()
