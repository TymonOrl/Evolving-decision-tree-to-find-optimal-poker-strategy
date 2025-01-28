from player import Player


class Phenotype:
    def __init__(self, index):
        self.index = index
        self.starting_balance = 0
        self.player = None
        self.wins = 0
        self.proc_gain = 0
        self.fitness = 0
        self.played_games = 0

    def __str__(self):
        output = f'Player {self.index}\n'
        output += f'Balance: {self.proc_gain}\n'
        output += f'Wins: {self.wins}\n'

        return output

    def reset_phenotype(self):
        self.wins = 0
        self.proc_gain = 0
        self.played_games = 0

    def calculate_fitness(self):
        # value of fitness is kept in range of [0, amount_of_players + 0.1*amount_of_rounds]
        self.fitness = (self.proc_gain/self.played_games) + 0.1 * (self.wins/self.played_games)
        return self.fitness

    def create_player(self, amount_of_players, starting_balance, max_depth=5):
        self.starting_balance = starting_balance
        self.player = Player(self.index, amount_of_players, starting_balance, max_depth)

    def save_results(self):
        self.wins += self.player.wins
        self.proc_gain += self.player.balance/self.starting_balance
        self.played_games += 1

    def mutate_leaf(self):
        tree = self.player.tree
        root = self.player.tree.root
        tree._mutate_random_leaf( root )

    def get_node_from_list(self, steps):
        tree = self.player.tree
        root = self.player.tree.root
        return tree.go_with_list(steps, 0, len(steps), root)

    def insert_node_from_list(self, steps, node):
        tree = self.player.tree
        root = self.player.tree.root
        self.player.tree.root = tree.insert_with_list(steps, 0, len(steps), root, node)
        return 1

    def visualise(self, name):
        tree = self.player.tree
        tree.visualize_tree(name)

    def get_player(self):
        return self.player

    def get_fitness(self):
        return self.fitness



