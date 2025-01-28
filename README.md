# Evolving-decision-tree-to-find-optimal-poker-strategy
Project toys with idea of creating fully randomly created decision trees and tuning them with genetic algorithms. Task for optimal decision tree is to classify what action should player take: Fold, Call or Rise. The decision is based of features, specified as:
- Score of the hand and cards on the table
- High card
- Amount on the table
- Which round of 10 is it
- How much did player already invest

Genetic algorithm here is very simple:
- Selection roulett based of fitness fucntion
- Crossover randomly switchs two branches or leafs
- Mutation changes value of a leaf

Project is very flawed, but achieves intresting results. The biggest problem is that algorithm is trained agains it self as it is unsupervised learing. Author recommends to change fitness function or try to evolve few tree parallel and than make them compete.

Project files:
- poker.py (is terminal based model created for this project)
- cards.py (is a class responsible for counting value of cards and handle deck actions)
- tree.py (is a implementation of fully random decision tree with genetic methods)
- player.py (is a class that participate in poker game. Each one has it's own tree)
- phenotype.py (is a class that repesent one specie in population and handles all actions related to genetic algorithms)
- population.py (is a class that handles whole generations and moving to the next, used as main)
