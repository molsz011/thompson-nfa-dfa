from thompson import *
from time import *

alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ '
numbers = '0123456789'
operators = '|^+*'
parentheses = '()'
valid_chars = alphabet + numbers + operators + parentheses
debug = False
debug2 = False


def validate_string(str):
    if str.count('(') != str.count(')'):
        exit('Amount of parentheses not matching.')

    if str is '':
        exit('No regular expression entered.')

    if str.count('(') == len(str)/2:
        exit('Cannot parese a string with only parentheses.')

    max_depth = str.count('(')
    higher = ''
    lower = ''

    parenthesis_depth = 0

    str += ' '

    level = 0
    for char in str:
        if level < 0:
            exit('Parentheses not matching.')
        elif char is '(':
            level += 1
        elif char is ')':
            level -= 1

    counter = 0
    for char in str:
        if counter == 0 and char in operators:
            exit('Invalid syntax: ' + char + str[counter + 1])
            return False
        if char not in valid_chars:
            exit('Invalid character: ' + char)
            return False
        if char == '(':
            if str[counter+1] in operators:
                exit('Invalid syntax: ' + char + str[counter+1])
                return False
            if parenthesis_depth != 0:
                higher += char
            elif str[counter-1] in operators:
                if debug:
                    print(str[counter-1])
            parenthesis_depth += 1
        elif char == '|':
            if str[counter + 1] in operators:
                exit('Invalid syntax: ' + char + str[counter + 1])
                return False
            if parenthesis_depth != 0:
                higher += char
            elif str[counter - 1] in operators:
                if debug:
                    print(str[counter - 1])
            parenthesis_depth += 1
        elif char == ')':
            if counter > 0:
                if str[counter-1] in '^|':
                    exit('Invalid syntax: ' + str[counter-1] + char)
                    return False
            if parenthesis_depth == 0:
                exit('Parenthesis error.')
                return False
            parenthesis_depth -= 1
            if parenthesis_depth != 0:
                higher += char
            elif str[counter+1] in operators:
                if debug:
                    print(str[counter+1])
        elif char == '*':
            if str[counter - 1] in '+*':
                exit('Invalid syntax: ' + str[counter - 1] + char)
                return False
            if parenthesis_depth != 0:
                higher += char
            elif str[counter - 1] in operators:
                if debug:
                    print(str[counter - 1])
        elif char == '+':
            if str[counter - 1] in '*+':
                exit('Invalid syntax: ' + str[counter - 1] + char)
                return False
            if parenthesis_depth != 0:
                higher += char
            elif str[counter - 1] in operators:
                if debug:
                    print(str[counter - 1])
        elif char == '^':
            if str[counter+1] not in numbers:
                exit('Invalid syntax: ' + char + str[counter + 1])
                return False
            else:
                if parenthesis_depth == 0:
                    lower += char
                else:
                    higher += char
                power = ''
                new_counter = counter
                new_counter += 1
                char = str[new_counter]
                while char.isnumeric():
                    power += char
                    if str[new_counter+1]:
                        new_counter += 1
                        char = str[new_counter]
                    else:
                        break
                if debug:
                    print(int(power))
        elif char in numbers and counter < len(str) - 1 and str[counter+1] in '*+':
            exit('Invalid syntax: ' + char + str[counter + 1])
            return False
        elif parenthesis_depth == 0:
            lower += char
        else:
            higher += char
        counter += 1

    if debug:
        print(lower + ' / ' + higher)
        if higher != '':
            validate_string(higher)
    return True

def add_parentheses_closure(str):
    if debug:
        print('doing *')
        print(str)
    counter = 0
    newstr = []
    for char in str:
        newstr.append(char)
        if char is '*':
            newstr.insert(counter+1, ')')
            if newstr[counter-1] in alphabet:
                newstr.insert(counter-1, '(')
                counter += 1
            elif newstr[counter-1] == ')':
                new_counter = counter
                level = 0
                while new_counter > 0 and (newstr[new_counter] != '(' or level > 0):
                    new_counter -= 1
                    if newstr[new_counter] is ')':
                        level += 1
                    if newstr[new_counter] is '(' and level > 0:
                        level -= 1
                newstr.insert(new_counter, '(')
                counter += 1
            elif newstr[counter-1] in numbers:
                newstr.insert(counter, ')')
                new_counter = counter
                level = 0
                while new_counter > 0 and (newstr[new_counter] in numbers+')^' or level > 0):
                    new_counter -= 1
                    if newstr[new_counter] is ')':
                        level += 1
                    if newstr[new_counter] is '(' and level > 0:
                        level -= 1
                newstr.insert(new_counter, '(')
                counter += 2

            counter += 1
        counter += 1
    if debug:
        print(counter)
    return newstr


def add_parentheses_positive_closure(str):
    if debug:
        print('doing +')
        print(str)
    counter = 0
    newstr = []
    for char in str:
        newstr.append(char)
        if char is '+':
            newstr.insert(counter+1, ')')
            if newstr[counter-1] in alphabet:
                newstr.insert(counter-1, '(')
                counter += 1
            elif newstr[counter-1] == ')':
                new_counter = counter
                level = 0
                while new_counter > 0 and (newstr[new_counter] != '(' or level > 0):
                    new_counter -= 1
                    if newstr[new_counter] is ')':
                        level += 1
                    if newstr[new_counter] is '(' and level > 0:
                        level -= 1
                newstr.insert(new_counter, '(')
                counter += 1
            elif newstr[counter-1] in numbers:
                newstr.insert(counter, ')')
                new_counter = counter
                level = 0
                while new_counter > 0 and (newstr[new_counter] in numbers+')^' or level > 0):
                    new_counter -= 1
                    if newstr[new_counter] is ')':
                        level += 1
                    if newstr[new_counter] is '(' and level > 0:
                        level -= 1
                newstr.insert(new_counter, '(')
                newstr.insert(new_counter, '(')
                counter += 2

            counter += 1
        counter += 1
    if debug:
        print(counter)
    return newstr


def add_parentheses_power(str):
    if debug:
        print('doing power')
        print(str)
    counter = 0
    iter = 0
    newstr = []
    char_skips = []
    skips = []
    char_skips_bool = False
    skips_bool = False
    while True:
        if debug:
            sleep(0.1)
        if iter < len(str):
            char = str[iter]
            if debug:
                print(char)
                print(''.join(newstr) + ' ' + counter.__str__())
            newstr.append(char)
        elif skips_bool or char_skips_bool:
            char = ''
            if not skips_bool:
                check = max(char_skips)
            elif not char_skips_bool:
                check = max(skips)
            else:
                check = max([max(char_skips), max(skips)])
            # print([max(char_skips), max(skips)])
            if check < 0:
                return newstr
        else:
            return newstr
        for idx in range(len(char_skips)):
            if debug:
                print(char_skips[idx])
            if char_skips[idx] > 0:
                char_skips[idx] -= 1
            elif char_skips[idx] == 0:
                newstr.append(')')
                counter += 1
                char_skips[idx] -= 1
        for idx in range(len(skips)):
            if debug:
                print(skips[idx])
            if skips[idx] > 0:
                skips[idx] -= 1
            elif skips[idx] == 0:
                newstr.append(')')
                counter += 1
                skips[idx] -= 1

        iter += 1
        if char is '^':
            new_counter = iter
            while new_counter < len(str) and str[new_counter] in numbers:
                if debug:
                    print('current: ' + str[new_counter])
                new_counter += 1
            if new_counter == iter:
                skips_bool = True
                skips.append(0)
            else:
                skips_bool = True
                skips.append(new_counter - iter - 1)
            if newstr[counter-1] in alphabet:
                newstr.insert(counter-1, '(')
                counter += 1
            elif newstr[counter-1] == ')':
                new_counter = counter
                level = 0
                while newstr[new_counter] != '(' or level > 0:
                    new_counter -= 1
                    if newstr[new_counter] is ')':
                        level += 1
                    if newstr[new_counter] is '(' and level > 0:
                        level -= 1
                newstr.insert(new_counter, '(')
                counter += 1

            counter += 1
        counter += 1

    if debug:
        print(counter)
    return newstr


def add_parentheses_or(str):
    if debug:
        print('doing OR')
        print(str)
    counter = 0
    iter = 0
    newstr = []
    char_skips = []
    skips = []
    char_skips_bool = False
    skips_bool = False
    while True:
        if debug:
            sleep(0.1)
        if iter < len(str):
            char = str[iter]
            if debug:
                print(char)
                print(''.join(newstr) + ' ' + counter.__str__())
            newstr.append(char)
        elif skips_bool or char_skips_bool:
            char = ''
            if not skips_bool:
                check = max(char_skips)
            elif not char_skips_bool:
                check = max(skips)
            else:
                check = max([max(char_skips), max(skips)])
            if check < 0:
                return newstr
        else:
            return newstr
        for idx in range(len(char_skips)):
            if debug:
                print(char_skips[idx])
            if char_skips[idx] > 0:
                char_skips[idx] -= 1
            elif char_skips[idx] == 0:
                newstr.append(')')
                counter += 1
                char_skips[idx] -= 1
        for idx in range(len(skips)):
            if debug:
                print(skips[idx])
            if skips[idx] > 0:
                skips[idx] -= 1
            elif skips[idx] == 0:
                newstr.append(')')
                counter += 1
                skips[idx] -= 1

        iter += 1
        if char is '|':
            if newstr[counter-1] in alphabet+'*+':
                new_counter = counter
                level = 0
                while new_counter > 0 and (newstr[new_counter] in alphabet + ')|' or level > 0):
                    new_counter -= 1
                    if newstr[new_counter] is ')':
                        level += 1
                    if newstr[new_counter] is '(':
                        level -= 1
                newstr.insert(new_counter, '(')
                counter += 1
            elif newstr[counter - 1] == ')':
                new_counter = counter
                level = 0
                while new_counter > 0 and (newstr[new_counter] in alphabet+')+*|' or level > 0):
                    new_counter -= 1
                    if newstr[new_counter] is ')':
                        level += 1
                    if newstr[new_counter] is '(':
                        level -= 1
                newstr.insert(new_counter, '(')
                counter += 1
            newstr.insert(counter, ')')
            counter += 2
            newstr.insert(counter, '(')
            new_counter = iter
            level = 0
            while new_counter < len(str) and (str[new_counter] in alphabet+'(|^'+numbers or level > 0):
                if debug:
                    print('current char: ' + str[new_counter])
                    print('level ' + level.__str__())
                if str[new_counter] is '(':
                    level += 1
                if str[new_counter] is ')':
                    level -= 1
                if new_counter >= len(str):
                    break
                new_counter += 1
            char_skips_bool = True
            char_skips.append(new_counter - iter)
        counter += 1
    if debug:
        print(counter)
        print(newstr)
    return newstr


def add_parentheses_concatenate(str):
    if debug:
        print('concatenating')
        print(str)
    counter = 0
    iter = 0
    newstr = []
    char_skips = []
    skips = []
    char_skips_bool = False
    skips_bool = False
    while True:
        if debug:
            sleep(0.1)
        if iter < len(str):
            char = str[iter]
            if debug:
                print(char)
                print(''.join(newstr) + ' ' + counter.__str__())
            newstr.append(char)
        elif skips_bool or char_skips_bool:
            char = ''
            if not skips_bool:
                check = max(char_skips)
            elif not char_skips_bool:
                check = max(skips)
            else:
                check = max([max(char_skips), max(skips)])
            if check < 0:
                return newstr
        else:
            return newstr
        for idx in range(len(char_skips)):
            if debug:
                print(char_skips[idx])
            if char_skips[idx] > 0:
                char_skips[idx] -= 1
            elif char_skips[idx] == 0:
                newstr.append(')')
                counter += 1
                char_skips[idx] -= 1
        for idx in range(len(skips)):
            if debug:
                print(skips[idx])
            if skips[idx] > 0:
                skips[idx] -= 1
            elif skips[idx] == 0:
                newstr.append(')')
                counter += 1
                skips[idx] -= 1

        iter += 1
        if debug:
            print('iter: ' + iter.__str__())
        if char in alphabet:
            if iter < len(str):
                if str[iter] in alphabet:
                    if iter > 1:
                        if str[iter] is '(':
                            if debug:
                                print('test ')
                            new_counter = counter
                            level = 0
                            while (newstr[new_counter] in valid_chars or level != 0) and new_counter > 1:
                                if newstr[new_counter-1] is ')':
                                    level += 1
                                if newstr[new_counter-1] is '(' and level > 0:
                                    level -= 1
                                new_counter -= 1
                            newstr.insert(new_counter, '(')
                            counter += 1
                            new_counter2 = iter
                            level = 0
                            while (str[new_counter2] in alphabet or level > 0) and new_counter2 < len(str) - 1:
                                if debug:
                                    print(new_counter2, level)
                                if str[new_counter2] is '(':
                                    level += 1
                                if str[new_counter2] is ')':
                                    level -= 1
                                new_counter2 += 1
                            skips_bool = True
                            skips.append(new_counter2 - iter)
                        else:
                            new_counter = counter
                            level = 0
                            while (newstr[new_counter-1] in alphabet+')' or level != 0) and new_counter > 0:
                                if newstr[new_counter-1] is ')':
                                    level += 1
                                if newstr[new_counter-1] is '(':
                                    level -= 1
                                new_counter -= 1
                            newstr.insert(new_counter, '(')
                            if newstr[counter] == ')':
                                newstr.append(')')
                                counter += 1
                            else:
                                skips_bool = True
                                skips.append(0)
                            counter += 1
                    else:

                        skips_bool = True
                        newstr.insert(counter, '(')
                        skips.append(0)
                        counter += 1


        counter += 1
    if debug:
        print(counter)
        print(newstr)
    return newstr
debug = False


def parenthesis_breakdown(string):
    if debug:
        sleep(0.2)
        print(string)
    skip = False
    strlist = []
    iter = 0
    newstr = ''
    while iter < len(string) and not skip:
        if string[iter] is '(':
            if newstr is not '':
                strlist.append(newstr)
                newstr = ''

            level = 0
            while True:
                if debug:
                    print('before: ' + str(level))
                    print(string[iter])
                if string[iter] is '(':
                    level += 1
                    if level == 1:
                        iter += 1
                        continue
                if string[iter] is ')':
                    level -= 1
                    if level == 0:
                        break
                newstr += string[iter]
                iter += 1
                if debug:
                    print('after: ' + str(level))
            strlist.append(newstr)
            newstr = ''
        elif string[iter] not in parentheses+operators:
            newstr += string[iter]
        elif string[iter] is '^':
            if newstr is not '':
                strlist.append(newstr)
                newstr = ''
            string += ' '
            while string[iter] in numbers+'^' and iter < len(string):
                newstr += string[iter]
                if debug:
                    print(string[iter])
                iter += 1
            string.rstrip()
            strlist.append(newstr)
            newstr = ''
            iter += 1

        elif string[iter] in operators:
            if newstr is not '':
                strlist.append(newstr)
                newstr = ''
            strlist.append(string[iter])


        iter += 1

    if newstr is not '':
        strlist.append(newstr)
    if debug2:
        print(strlist)
    ret = None
    prev = None
    iter2 = 0
    while iter2 < len(strlist):
        curr = strlist[iter2]
        if len(curr) == 2 and curr[0] in alphabet and curr[1] in alphabet:
            if debug2:
                print('concatenating ' + curr[0] + ' and ' + curr[1])
            temp = thompson_concatenate(curr[0], curr[1])
            if iter2 == 0 or ret is None:
                ret = temp
            else:
                ret = thompson_concatenate(ret, temp)
        elif len(curr) == 1 and curr in alphabet:
            temp = str2auto(str(curr[0]))
            if debug2:
                print('creating: ' + temp.name)
            # sleep(1)
            if iter2 == 0 or ret is None:
                ret = temp
            else:
                prev = ret
                ret = thompson_concatenate(ret, temp)
        elif curr is '|':
            if debug2:
                print('ORing ' + ret.name + ' ' + str(strlist[iter2+1:len(strlist)]))
            temp = thompson_or(ret, parenthesis_breakdown(strlist[iter2+1:len(strlist)]))
            if iter2 == 0 or prev is None:
                prev = temp
                ret = temp
                return ret
            else:
                # prev = ret
                ret = temp
                return ret
            iter2 += 1
        elif curr is '*':
            if debug2:
                print('performing closure on ' + curr)
            temp = thompson_closure(parenthesis_breakdown(strlist[iter2-1]))
            if iter2 == 0 or prev is None:
                prev = temp
                ret = temp
            else:
                ret = thompson_concatenate(prev, temp)
        elif curr is '+':
            if debug2:
                print('performing positive closure on ' + curr)
            temp = thompson_positive_closure(parenthesis_breakdown(strlist[iter2-1]))
            if iter2 == 0 or prev is None:
                prev = temp
                ret = temp
            else:
                prev = ret
                ret = thompson_concatenate(prev, temp)
        elif curr[0] is '^':
            power = str(curr.replace('^', ''))
            if debug2:
                print('repeating ' + strlist[iter2-1] + ' ' + power + ' times')
            temp = thompson_power(parenthesis_breakdown(strlist[iter2-1]), power)
            if iter2 == 0 or prev is None:
                prev = temp
                ret = temp
            else:
                # prev = ret
                ret = thompson_concatenate(prev, temp)

        elif len(strlist) == 1:
            if debug2:
                print('breaking down2 ' + curr)
            return parenthesis_breakdown(curr)

        else:
            temp = parenthesis_breakdown(curr)
            if iter2 == 0 or ret is None:
                ret = temp
            else:
                prev = ret
                ret = thompson_concatenate(ret, temp)
        iter2 += 1
        if debug2:
            print(ret)
            ret.display(string)
    return ret


def str_to_nfa(strn):
    clos = add_parentheses_closure(strn)
    pclos = add_parentheses_positive_closure(clos)
    power = add_parentheses_power(pclos)
    conc = add_parentheses_concatenate(power)
    stror = add_parentheses_or(conc)
    newstr = ''.join(stror)
    aut = parenthesis_breakdown(newstr)
    return aut