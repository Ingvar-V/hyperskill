import random

user_name = input('Enter your name: ')
print(f'Hello, {user_name}')
game_set = list(input().split(','))
if game_set == ['']:
    game_set = ['rock', 'paper', 'scissors']
print("Okay, let's start")
user_score = 0
file = open('rating.txt')
for item in file:
    user, score = item.split()
    if user == user_name:
        user_score = int(score)
        break
file.close()
while True:
    user_choice = input()
    if user_choice == '!exit':
        print('Bye!')
        exit()
    elif user_choice == '!rating':
        print(f'Your rating: {user_score}')
        continue
    elif user_choice in game_set:
        comp_choice = random.choice(game_set)
        if user_choice == comp_choice:
            print(f'There is a draw ({user_choice})')
            user_score += 50
        else:
            shift = (game_set.index(comp_choice) - game_set.index(user_choice)) % len(game_set)
            if shift > len(game_set) // 2:
                user_score += 100
                print(f'Well done. The computer chose {comp_choice} and failed')
            else:
                print(f'Sorry, but the computer chose {comp_choice}')
    else:
        print('Invalid input')
