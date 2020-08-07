def print_field(elements):
    print(9 * '-')
    print('|', ' '.join(elements[:3]), '|')
    print('|', ' '.join(elements[3:6]), '|')
    print('|', ' '.join(elements[6:]), '|')
    print(9 * '-')

def outcome(elements):
    game_state = ''
    if abs(elements.count('X') - elements.count('O')) > 1 or (['X', 'X', 'X'] in straights and ['O', 'O', 'O'] in straights):
        game_state = 'Impossible'
    elif ['X', 'X', 'X'] in straights:
        game_state = 'X wins'
    elif ['O', 'O', 'O'] in straights:
        game_state = 'O wins'
    elif elements.count(' ') > 0:
        game_state = 'Game not finished'
    elif elements.count(' ') == 0:
        game_state = 'Draw'
    return game_state

positions = [13, 23, 33, 12, 22, 32, 11, 21, 31]
elem_list = list(' ' * 9)
elem_array = dict(zip(positions, elem_list))
X_O_Turn = 1
print_field(elem_list)
while True:
    turn = input('Enter the coordinates: ').split()
    if turn[0].isdigit() and turn[1].isdigit():
        if int(turn[0]) > 3 or int(turn[1]) > 3:
            print('Coordinates should be from 1 to 3!')
        elif elem_array[int(turn[0] + turn[1])] != ' ':
            print('This cell is occupied! Choose another one!')
        else:
            if X_O_Turn % 2 == 0:
                elem_array[int(turn[0] + turn[1])] = 'O'
            else:
                elem_array[int(turn[0] + turn[1])] = 'X'
            X_O_Turn += 1
            elements = [v for v in elem_array.values()]
            straights=[elements[:3], elements[3:6], elements[6:], elements[::3], elements[1::3], elements[2::3],
            elements[::4], elements[2:7:2]]
            print_field(elements)
            result = outcome(elements)
            if result in ['X wins', 'O wins', 'Draw']:
                print(result)
                break
    else:
        print("You should enter numbers!")
