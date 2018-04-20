from dfa import *

regex = input('Please enter the regular expression: ')

if not validate_string(regex):
    exit('The string ' + regex + ' cannot be parsed.')

auto = str_to_nfa(regex)
auto.display(regex)

dfa = nfa_to_dfa(auto)
dfa.display(regex)
inp = ''
print('Enter strings to check if they are accepted by the automata.')
print('Type !quit to quit.')
while True:
    inp = input('Please enter a string: ')
    if inp == '!quit':
        exit('Exiting.')
    elif check_str(dfa, inp):
        print('The string is accepted.')
    else:
        print('The string is not accepted.')