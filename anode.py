class Anode():
    def __init__(self, label):
        self.label = label
        self.connections = {}
        self.nfa_states = []

    def add_connection(self, destination, label):
        self.connections[destination] = label

    def display_connections(self):
        for dest, label in self.connections.items():
            print(dest + ": " + label)

