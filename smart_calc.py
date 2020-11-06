import re
from collections import deque, Counter


# Stack class
class Stack:
    def __init__(self, size):
        self.stack = []
        self.size = size

    def push(self, item):
        if len(self.stack) < self.size:
            self.stack.append(item)

    def pop(self):
        result = -1
        if self.stack:
            result = self.stack.pop()
        return result

    def display(self):
        if not self.stack:
            print('Stack is empty!')
        else:
            print('Stack data:')
            for item in reversed(self.stack):
                print(item)

    def is_empty(self):
        return self.stack == []

    def top_char(self):
        result = -1
        if self.stack:
            result = self.stack[len(self.stack) - 1]
        return result


# Aux operations
def is_operand(c):
    return re.search(r'[a-zA-Z0-9]', c)


operators = '+-*/^'


def is_operator(c):
    return c in operators


def get_precedence(c):
    result = 0
    for char in operators:
        result += 1
        if char == c:
            if c in '-/':
                result -= 1
            break
    return result

calc_dict ={}


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# infix to postfix
def to_postfix(expression):
    result = ''
    for elem in expression:
        if elem in calc_dict.keys():
            expression = re.sub(elem, calc_dict[elem], expression)
    expression = re.sub('\(', '( ', expression)
    expression = re.sub('\)', ' )', expression)
    expression = expression.split()
    stack = Stack(50)
    for char in expression:
        if char.isdigit():
            result += char + ' '
        elif is_operator(char):
            while True:
                top_char = stack.top_char()

                if stack.is_empty() or top_char == '(':
                    stack.push(char)
                    break
                else:
                    pC = get_precedence(char)
                    pTC = get_precedence(top_char)

                    if pC > pTC:
                        stack.push(char)
                        break
                    else:
                        result += stack.pop() + ' '

        elif char == '(':
            stack.push(char)
        elif char == ')':
            cpop = stack.pop()
            while cpop != '(':
                result += cpop + ' '
                cpop = stack.pop()
    while not stack.is_empty():
        cpop = stack.pop()
        result += cpop
    return result


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Evaluate Postfix expression
def eval_expression(expr):
    arr_list = expr.split()
    stack=[]

    for item in arr_list:
        if item not in operators:
            stack.append((item))
        else:
            first = int(stack.pop())
            sec = int(stack.pop())

            if item == "+":
                stack.append(sec + first)

            if item == "-":
                stack.append(sec - first)

            if item == "*":
                stack.append(sec * first)

            if item == "/":
                stack.append(sec / first)
    return stack[-1]


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
while True:
    user_input = input()
    if not user_input:
        continue
    elif re.search(r'^/', user_input):
        if user_input == '/exit':
            print('Bye!')
            exit()
        elif user_input == '/help':
            print('The program calculates sum, difference, multiplication and integer division of numbers')
            continue
        else:
            print('Unknown command')
            continue
    elif len(re.findall('\(', user_input)) != len(re.findall('\)', user_input)):
        print('Invalid expression')
        continue
    elif (Counter(user_input)['*'] or Counter(user_input)['/']) > 1:
        print('Invalid expression')
        continue
    elif re.search(r'=', user_input):
        if user_input.count('=') > 1:
            print('Invalid assignment')
            continue
        user_input = re.split(r'=', user_input)
        if re.search(r'[a-zA-Z]', user_input[1]):
            if re.search(r'[a-zA-Z]', user_input[1]) and re.search(r'[0-9]', user_input[1]):
                print('Invalid assignment')
            val = re.sub(r' ', '', user_input[1])
            if val in calc_dict.keys():
                key = re.sub(r' ', '', user_input[0])
                calc_dict[key] = calc_dict[val]
            else:
                print('Unknown variable')
            continue
        elif re.search(r'[a-zA-Z]', user_input[0]) and not re.search(r'[0-9]', user_input[0]):
            key = re.sub(r' ', '', user_input[0])
            calc_dict[key] = user_input[1].lstrip()
        else:
            print('Invalid identifier')
    elif re.search(r'[+-/*]', user_input):
        print(eval_expression(to_postfix(user_input)))
        continue
    elif re.search(r'[a-zA-Z]', user_input):
        if user_input in calc_dict.keys():
            print(calc_dict[user_input])
        else:
            print('Unknown variable')
        continue
