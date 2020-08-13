import random
import re

print('H A N G M A N')
while True:
    menu = input('Type "play" to play the game, "exit" to quit: ')
    if menu == 'play':
        print()
        try_cnt = 8
        user_letters = set()
        words_list = ['python', 'java', 'kotlin', 'javascript']
        riddle = list(random.choice(words_list))
        hidden_word = list(len(riddle) * "-")
        while try_cnt > 0:
            print()
            print(''.join(hidden_word))
            letter = input('Input a letter: ')
            if len(letter) != 1:
                print('You should input a single letter')
                continue
            elif re.search(r'[^a-z]', letter):
                print('It is not an ASCII lowercase letter')
                continue
            letter_cnt = riddle.count(letter)
            if letter in user_letters:
                print('You already typed this letter')
            elif letter_cnt:
                for _ in range(letter_cnt):
                    hidden_word[riddle.index(letter)] = letter
                    riddle[riddle.index(letter)] = '*'
            else:
                print('No such letter in the word')
                try_cnt -= 1
            user_letters.add(letter)
        if try_cnt > 0:
            print('You guessed the word!')
            print("You survived!")
        else:
            print('You are hanged!')
    else:
        exit()
