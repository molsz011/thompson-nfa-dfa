#### Simple application for converting regular expressions into non-deterministic and deterministic finite automata.

##### Input string syntax: 
1. letters (abc...xyz) - characters from the alphabet 
2. xy - concatenation of x and y 
3. x^n (n = number) - string x repeated n times 
4. x* - closure (any number of string x) 
5. x+ - positive closure (any number of string x, excluding 0) 
6. x|y - x or y 7. () - parentheses to group expressions 
 
##### Precedence rules: 
1. () - expression within brackets 
2. \* - closure 
3. \+ - positive closure 
4. ^n - repetition 
5. concatenation 
6. | - alternative 
 
The application requires Graphviz (https://www.graphviz.org/) and its Python library for graph visualization.

##### Example usage:
`Please enter the regular expression: (ab)(c|d)*`

We obtain the following graphs:

Non-deterministic:

![NFA](https://github.com/molsz011/thompson-nfa-dfa/blob/master/media/nfa.png "NFA")

Deterministic:

![DFA](https://github.com/molsz011/thompson-nfa-dfa/blob/master/media/dfa.png "DFA")

Now we can enter strings to check whether they are accepted by the automaton:
```Enter strings to check if they are accepted by the automata.
Type !quit to quit.
Please enter a string: abc
The string is accepted.
Please enter a string: abcdcd
The string is accepted.
Please enter a string: acd
The string is not accepted.
Please enter a string: !quit
Exiting.