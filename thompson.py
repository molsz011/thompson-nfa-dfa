from automata import Automata
from anode import Anode
from copy import deepcopy

debug = False
# debug = True

def str2auto(aut1):
    auto1 = Automata(aut1)
    auto1.add_node(1)
    auto1.add_node(2)
    auto1.add_connection(1, 2, aut1)
    auto1.final_state = 2
    return auto1


def thompson_concatenate(aut1, aut2):

    if type(aut1) == Automata:
        str1 = aut1.name
        auto1 = aut1
    else:
        str1 = aut1
        auto1 = str2auto(aut1)

    if type(aut2) == Automata:
        str2 = aut2.name
        auto2 = aut2
    else:
        str2 = aut2
        auto2 = str2auto(aut2)

    if debug:
        auto1.display()
        auto2.display()

    auto3 = Automata('(' + str1 + str2 + ')')
    auto3.set_initial_state(auto1.initial_state)
    auto3.set_final_state(auto1.final_state + auto2.final_state - 1)

    for node in auto1.node_list:
        if node.label != auto1.final_state:
            auto3.node_list.append(node)

    for node in auto2.node_list:
        new_node = Anode(node.label + int(auto1.final_state-1))
        for dest, label in node.connections.items():
            new_node.add_connection(dest+int(auto1.final_state)-1, label)
        auto3.node_list.append(new_node)

    return auto3


def thompson_or(aut1, aut2):
    if type(aut1) == Automata:
        str1 = aut1.name
        auto1 = aut1
    else:
        str1 = aut1
        auto1 = str2auto(aut1)

    if type(aut2) == Automata:
        str2 = aut2.name
        auto2 = aut2
    else:
        str2 = aut2
        auto2 = str2auto(aut2)

    if debug:
        auto1.display()
        auto2.display()

    auto3 = Automata('(' + str1 + "OR" + str2 + ')')

    auto3.add_node(1)
    auto3.add_node(auto1.final_state + auto2.final_state + 2)

    auto3.set_initial_state(1)
    auto3.set_final_state(auto1.final_state + auto2.final_state + 2)

    for node in auto1.node_list:
        new_node = Anode(node.label + 1)
        for dest, label in node.connections.items():
            new_node.add_connection(dest + 1, label)
        if node.label == auto1.final_state:
            new_node.add_connection(auto3.final_state, 'eps')
        auto3.node_list.append(new_node)

    for node in auto2.node_list:
        new_node = Anode(node.label + int(auto1.final_state) + 1)
        for dest, label in node.connections.items():
            new_node.add_connection(dest + int(auto1.final_state) + 1, label)
        if node.label == auto2.final_state:
            new_node.add_connection(auto3.final_state, 'eps')
        auto3.node_list.append(new_node)

    auto3.add_connection(1, 2, 'eps')
    auto3.add_connection(1, 2 + int(auto1.final_state), 'eps')

    return auto3

def thompson_closure(aut1):
    if type(aut1) == Automata:
        str1 = aut1.name
        auto1 = aut1
    else:
        str1 = aut1
        auto1 = str2auto(aut1)

    if debug:
        auto1.display()

    auto3 = Automata('(' + str1 + '-closure)')

    auto3.add_node(1)
    auto3.add_node(auto1.final_state + 2)

    auto3.set_initial_state(1)
    auto3.set_final_state(auto1.final_state + 2)

    for node in auto1.node_list:
        new_node = Anode(node.label + 1)
        for dest, label in node.connections.items():
            new_node.add_connection(dest + 1, label)
        if node.label == auto1.final_state:
            new_node.add_connection(2, 'eps')
            new_node.add_connection(auto3.final_state, 'eps')
        auto3.node_list.append(new_node)

    auto3.add_connection(1, 2, 'eps')
    auto3.add_connection(1, auto3.final_state, 'eps')

    return auto3

def thompson_positive_closure(aut1):
    if type(aut1) == Automata:
        str1 = aut1.name
        auto1 = aut1
    else:
        str1 = aut1
        auto1 = str2auto(aut1)

    if debug:
        auto1.display()

    auto3 = Automata('(' + str1 + '+)')

    auto3.add_node(1)
    auto3.add_node(auto1.final_state + 2)

    auto3.set_initial_state(1)
    auto3.set_final_state(auto1.final_state + 2)

    for node in auto1.node_list:
        new_node = Anode(node.label + 1)
        for dest, label in node.connections.items():
            new_node.add_connection(dest + 1, label)
        if node.label == auto1.final_state:
            new_node.add_connection(2, 'eps')
            new_node.add_connection(auto3.final_state, 'eps')
        auto3.node_list.append(new_node)

    auto3.add_connection(1, 2, 'eps')

    return auto3


def thompson_power(aut1, rep):
    if type(aut1) == Automata:
        str1 = aut1.name
        auto1 = aut1
    else:
        str1 = aut1
        auto1 = str2auto(aut1)

    if debug:
        auto1.display()
    repeats = int(rep)
    name = '(' + str1 + '^' + str(repeats) + ')'
    if repeats == 0:
        auto3 = Automata(name)
        auto3.add_node(1)
        auto3.add_node(2)
        auto3.add_connection(1, 2, 'eps')
        auto3.set_initial_state(1)
        auto3.set_final_state(2)
        return auto3
    elif repeats == 1:
        auto3 = deepcopy(auto1)
        auto3.name = name
        return auto3
    else:
        auto3=deepcopy(auto1)
        for i in range(1, repeats):
            for node in auto1.node_list:
                new_node = Anode(node.label + (auto1.final_state * i))
                for dest, label in node.connections.items():
                    new_node.add_connection(dest + (auto1.final_state * i), label)
                auto3.node_list.append(new_node)
            auto3.add_connection(auto1.final_state * i, (auto1.final_state * i) + 1, 'eps')
        auto3.set_final_state(auto1.final_state * repeats)
        auto3.name = name
        return auto3