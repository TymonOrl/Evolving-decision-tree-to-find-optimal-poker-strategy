import numpy as np
from graphviz import Digraph
from enum import Enum

class Features(Enum):
    HAND_SCORE = 0
    HIGH_CARD_SCORE = 1
    BET = 2
    BALANCE = 3
    AMOUNT_PLACED = 4
    ROUND = 5


class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None,*,value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.value = value
        

    def is_leaf_node(self):
        return self.value is not None


class DecisionTree:
    def __init__(self, 
                    min_samples_split=2, 
                    max_depth=5, 
                    M_treshholds = np.array([[0,0,0,0,0],[9,12,10240,10240,4]]),
                    n_features=None):
        self.min_samples_split=min_samples_split
        self.max_depth=max_depth
        self.n_features=n_features
        self.root=None
        self.M_treshholds = M_treshholds


    def create(self, x, labels):
        self.root = self._grow_tree(x, labels)


    def _grow_tree(self, features, labels, depth=0):

        # Check the stopping criteria
        if (depth>=self.max_depth):
            leaf_value = self._random_label(labels)
            return Node(value=leaf_value)

        # Create random splits
        new_feature, new_thresh = self._new_split(len(labels))

        # Create child nodes
        left = self._grow_tree(features, labels, depth+1)
        right = self._grow_tree(features, labels, depth+1)
        return Node(new_feature, new_thresh, left, right)


    def _new_split(self, len_labels):
        # chooses random feature and random trashhold with respect to M
        split_idx, split_threshold = None, None
        split_idx = np.random.choice(len_labels)
        split_threshold = np.random.randint(
            self.M_treshholds[0,split_idx], self.M_treshholds[1,split_idx])

        return split_idx, split_threshold


    def _random_label(self, labels):
        value = np.random.choice(labels)
        return value


    def predict(self, X):
        return self._traverse_tree(X, self.root)


    def _traverse_tree(self, x, node):
        if node.is_leaf_node():
            return node.value

        if x[node.feature] <= node.threshold:
            return self._traverse_tree(x, node.left)
        return self._traverse_tree(x, node.right)


    def go_with_list(self, steps, step, amount_of_steps, node):
        if step == amount_of_steps-1:
            if steps[step] <= 0.5:
                return node.left
            return node.right

        step += 1
        if steps[step] <= 0.5:
            return self.go_with_list(steps, step, amount_of_steps, node.left)
        return self.go_with_list(steps, step, amount_of_steps, node.right)
    

    def insert_with_list(self, steps, step, amount_of_steps, node, insert_node):
        if step == amount_of_steps-1:
            if steps[step] <= 0.5:
                node.left = insert_node
                return self.root
            node.right = insert_node
            return self.root

        step += 1
        if steps[step] <= 0.5:
            return self.insert_with_list(steps, step, amount_of_steps, node.left, insert_node)
        return self.insert_with_list(steps, step, amount_of_steps, node.right, insert_node)


    def _mutate_random_leaf(self, node):
        labels = [0,1,2]
        if node.is_leaf_node():
            old_value = node.value
            node.value = self._random_label(labels)
            while old_value == node.value:
                node.value = self._random_label(labels)

            return node.value

        if np.random.rand() <= 0.5:
            return self._mutate_random_leaf(node.left)
        return self._mutate_random_leaf(node.right)


    def _add_nodes_edges(self, dot, node, parent=None, edge_label=""):
        if node is None:
            return
        
        # Create a unique label for the current node
        node_label = f"Node {id(node)}\n"
        if node.is_leaf_node():
            node_label += f"Value: {node.value}"
        else:
            node_label += f"Feature: {Features(node.feature).name}\nThreshold: {node.threshold:.2f}"
        
        dot.node(str(id(node)), label=node_label)

        # Add an edge from parent to this node (if applicable)
        if parent:
            dot.edge(str(id(parent)), str(id(node)), label=edge_label)
        
        # Recurse for children
        if not node.is_leaf_node():
            self._add_nodes_edges(dot, node.left, node, edge_label="True")
            self._add_nodes_edges(dot, node.right, node, edge_label="False")

    def visualize_tree(self, name):
        # Usage of graphviz librarry
        dot = Digraph()
        self._add_nodes_edges(dot, self.root)
        dot.render(name, format="png", cleanup=True)
        return dot

'''
# Testing
x = np.zeros(5)
labels = [0,1,2]
test = DecisionTree(max_depth=4)
test.create(x, labels)
test.visualize_tree('test')
'''