from anode import Anode
import graphviz as gv
import os

class Automata():
    def __init__(self, name):
        self.name = name
        self.node_list = []
        self.initial_state = None
        self.final_state = None
        self.final_states = []

    def add_node(self, label, nodes=None):
        my_node = Anode(label)
        if nodes is None:
            my_node.nfa_states = []
        else:
            my_node.nfa_states = nodes
        self.node_list.append(my_node)
        if self.initial_state is None:
            self.initial_state = label
            self.final_state = label


    def add_connection(self, label, dest, symbol):
        flag = False
        for node in self.node_list:
            if dest == node.label:
                flag = True
                break
        if not flag:
            print(str(dest) + ' is not a valid node')
            return
        for node in self.node_list:
            if label == node.label:
                node.add_connection(dest, symbol)
                return
        print(str(label) + ' is not a valid node')

    def display(self, regex):
        if self.final_states == []:
            lab = 'NFA: ' + ''.join(regex)
        else:
            lab = 'DFA: ' + ''.join(regex)
        g1 = gv.Digraph(format='svg')
        g1.attr(rankdir = 'LR')
        g1.attr(label = lab)
        for node in self.node_list:
            if node.label == self.initial_state:
                g1.attr('node', shape='rarrow')
            elif node.label == self.final_state or node.label in self.final_states:
                g1.attr('node', shape='doublecircle')
            else:
                g1.attr('node', shape='circle')
            g1.node(str(node.label))

        for node in self.node_list:
            for aconn, alabel in node.connections.items():
                g1.edge(str(node.label), str(aconn), label=str(alabel))

        filename = g1.render(filename='img/' + self.name)
        os.startfile(os.getcwd() + "/" + filename)

    def set_initial_state(self, label):
        self.initial_state = label

    def set_final_state(self, label):
        self.final_state = label