from thompson import *
from string_parser import *

def eps_closure(auto, states, checked):
    if type(states) == list:
        eps_states = states
    else:
        eps_states = []
        eps_states.append(states)
        states = eps_states
    if checked == []:
        chk = []
    else:
        chk = checked

    for state in states:
        for node in auto.node_list:
            if node.label == state:
                current_node = node
                break
        for dest, label in current_node.connections.items():
            if label == 'eps' and dest not in eps_states and dest not in chk:
                eps_states.append(dest)
                chk.append(dest)
                temp = eps_closure(auto, dest, chk)
                for state in temp:
                    if state not in eps_states:
                        eps_states.append(state)

    return sorted(eps_states)

def move(auto, node, label):
    move_states = []
    for state in node.nfa_states:
        for n in auto.node_list:
            if n.label == state:
                current_node = n
                break
        for dest, l in current_node.connections.items():
            if l == label:
                move_states.append(dest)
    return move_states


def nfa_to_dfa(auto):
    labels = []
    current = 'A'
    for node in auto.node_list:
        for dest, label in node.connections.items():
            if label not in labels and label != 'eps':
                labels.append(label)
    name = 'DFA ' + auto.name
    dfa1 = Automata(name)
    dfa1.add_node('A', eps_closure(auto, 1, []))
    if auto.final_state in dfa1.node_list[0].nfa_states:
        dfa1.final_states.append('A')
    number_of_nodes = 1
    i = 0
    while i < number_of_nodes:
        node = dfa1.node_list[i]
        for label in labels:
            unique = True
            mov = move(auto, node, label)
            eps_cl = eps_closure(auto, mov, [])
            if eps_cl == []:
                continue
            for n in dfa1.node_list:
                if n.nfa_states == eps_cl:
                    frm = node.label
                    to = n.label
                    unique = False
            if unique:
                old = current
                new = ord(current)
                new += 1
                current = chr(new)
                frm = node.label
                to = current
                dfa1.add_node(current, eps_cl)
                if auto.final_state in eps_cl:
                    dfa1.final_states.append(current)
                number_of_nodes += 1
            dfa1.add_connection(frm, to, label)

        i += 1
    return dfa1


def check_str(dfa, strn):
    if type(strn) != str:
        exit('The parameter has to be a string.')
    current_node = dfa.node_list[0]

    if strn is '':
        if current_node.label in dfa.final_states:
            return True
        else:
            return False
    i = 0

    while i < len(strn):
        next_node = None
        for dest, label in current_node.connections.items():
            if label == strn[i]:
                next_node = dest
                break
        if next_node is None:
            return False
        else:
            for node in dfa.node_list:
                if node.label == next_node:
                    current_node = node
        i += 1

    if current_node.label in dfa.final_states:
        return True
    else:
        return False

