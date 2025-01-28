import numpy as np
from tree import Node, DecisionTree
from poker import play_game
from player import Player_actions
from phenotype import Phenotype
import matplotlib.pyplot as plt
import copy

class Population:
    def __init__(self, population_size, max_depth):
        self.population_size = population_size
        self.max_depth = max_depth
        self.labels = np.arange( len(Player_actions) )

        # Statistic
        self.fitness = []
        self.best_fitness = []

        # Game rules
        # Warning!
        # There is no safety for having amount of players that can't devide population whithout rest
        self.amount_of_players = 10
        self.starting_balance = 2000
        self.amount_of_rounds = 10
        self.amount_of_tournaments = 100

        self.population = [Phenotype(i) for i in range(self.population_size)]
        for phenotype in self.population:
            phenotype.create_player(self.amount_of_players, self.starting_balance, max_depth = self.max_depth)


    def calculate_fitness(self):
        self.fitness = [ phenotype.calculate_fitness() for phenotype in self.population]


    def add_best_fitness(self):
        self.best_fitness.append( np.max(self.fitness) )


    def get_best_phenotype(self):
        return self.population[ np.argmax(self.fitness) ]


    def play(self):
        # Reset balances and wins
        for phenotype in self.population:
            phenotype.reset_phenotype()

        amount_of_parallel_games = int(self.population_size/self.amount_of_players)

        for i_tournament in range(self.amount_of_tournaments):
            if i_tournament%100 == 0:
                print(f'Round: {i_tournament}')
            # Random selection of oponents
            indexes = np.arange(0, self.population_size, dtype=np.int32)
            np.random.shuffle(indexes) 

            players = [phenotype.get_player() for phenotype in self.population]
            for i in range(0, amount_of_parallel_games):
                for n_round in range(self.amount_of_rounds):
                    idx = indexes[i*self.amount_of_players:(i+1)*self.amount_of_players]
                    tmp_players = []
                    for tmp_idx in idx:
                        tmp_players.append(players[tmp_idx])

                    tmp_players = play_game( tmp_players, self.amount_of_rounds )
                    for player in tmp_players:
                        self.population[player.index].save_results()
                        self.population[player.index].player.reset_player()
                

    def selection(self, mode):
        fitness_sum = np.array(self.fitness).sum()

        if mode == "roulette":
            fitness_percentages = [fitness / fitness_sum for fitness in self.fitness]
            mating_pool = []

            for _ in range(self.population_size):
                random_number = np.random.rand()
                for i in range(self.population_size):
                    if random_number < sum(fitness_percentages[:i+1]):
                        mating_pool.append(self.population[i])
                        break
                
        return mating_pool

    
    def crossover(self, mating_pool):
        parents1 = mating_pool[:int(self.population_size/2)]
        parents2 = mating_pool[int(self.population_size/2):]

        children = []
        for i in range(len(parents1)):
            parent_1 = parents1[i]
            parent_2 = parents2[i]
            child_1 = copy.deepcopy(parents1[i])
            child_2 = copy.deepcopy(parents2[i])

            list_length = np.random.randint(1, self.max_depth)
            list_of_random_turns_1 = np.random.rand(list_length)
            list_of_random_turns_2 = np.random.rand(list_length)

            node_1 = child_1.get_node_from_list(list_of_random_turns_1)
            node_2 = child_2.get_node_from_list(list_of_random_turns_2)

            child_1.insert_node_from_list(list_of_random_turns_1, node_2)
            child_2.insert_node_from_list(list_of_random_turns_2, node_1)
            
            children.append(child_1)
            children.append(child_2)
            
        return children
    

    def mutation(self, children, chance):
        for child in children:
            if np.random.random() <= chance:
                child.mutate_leaf()

        return children
    

    def evolve(self, amount_of_epochs, mutation_rate):
        self.play()
        self.calculate_fitness()
        for i in range(amount_of_epochs+1):
            print(f'Epoch: {i}')
            if i == amount_of_epochs:
                self.epoch(mutation_rate, end=True)
            else:    
                self.epoch(mutation_rate)

        plt.plot(self.best_fitness)
        plt.show()

        best_phenotype = self.get_best_phenotype()
        print(best_phenotype.player.balance)
        print(best_phenotype.player.wins)
        best_phenotype.visualise('Best')


    def epoch(self, mutation_rate, end=False):
        self.play()
        if end==False:
            mating_pool = self.selection("roulette")
            mating_pool = [pop for pop in self.population]
            children = self.crossover(mating_pool)
            children = self.mutation(children, mutation_rate)
            self.population = children
        self.calculate_fitness()
        self.add_best_fitness()

main_pop = Population(1000, 5)
main_pop.evolve(10, 0.05)

