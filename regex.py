import sys
sys.setrecursionlimit(6000)


# сравниваем символы
def char_match(pattern, char):
    if pattern == '.':     # если шаблон точка, то возвращаем ИСТИНА
        return True
    return pattern == char # возращаем ИСТИНА/ЛОЖь в завис-ти от того совпадает ли смивол в слове и шаблоне

# Сравниваем слово одинаковой длины. Вызываем char_match для каждого символа рекурсивно
def word_match(pattern, word):
    if pattern == '':
        return True

    if word == '':
        if pattern == '$':
            return True
        else:
            return False

    if len(pattern) == 1:
        return char_match(pattern[0], word[0])

    # проверяем символ ?
    if pattern[1] == '?':
        if pattern[0] == '\\':
            word = word[1:]
        return word_match(pattern[2:], word) or\
               word_match(pattern[0] + pattern[2:], word)

    # проверяем символ *
    if pattern[1] == '*':
        return word_match(pattern[2:], word) or\
               word_match(pattern, word[1:])
    #проверяем символ +
    if pattern[1] == '+':
        return word_match(pattern[0] + pattern[2:], word) or\
            word_match(pattern,word[1:])


    if pattern[0] == '\\':
        return word_match(pattern[1], word)

    if not char_match(pattern[0], word[0]):
        return False

    return word_match(pattern[1:], word[1:])


# Сравниваем строку произвольной длины с шаблоном
def string_match(pattern, string):
    if not pattern:
        return True

    if not string:
        return False

    # начинается с ^
    if pattern[0] == '^':
        return word_match(pattern[1:], string)

    if word_match(pattern, string):
        return True

    return string_match(pattern, string[1:])

if __name__ == '__main__':
    rexp, val = input().split('|')
    print(string_match(rexp, val))
