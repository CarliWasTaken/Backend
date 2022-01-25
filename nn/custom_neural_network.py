from typing import *

import numpy as np
import scipy.special
import matplotlib.pyplot as plt
import random

# random.seed(1)
# np.random.seed(1)

class CustomNeuralNetwork:
    def __init__(self, input_nodes :int, hidden_nodes :int, output_nodes :int, learning_rate :float, weights :Tuple[np.ndarray, np.ndarray]=None):
        '''Creates a wonderful Neural Network (NN)
        
        Parameters
        
            input_nodes :int
                The number of input nodes
            hidden_nodes :int
                The number of hidden nodes
            output_nodes :int
                The number of output nodes
            learning_rate :float
                The learning rate of the network
            weights :Tuple[np.ndarray, np.ndarray], optional
                The weights of the network. If not given, the weights are initialized randomly
                Structure: (weights_input_hidden, weights_hidden_output)
        
        '''
  
        self.i_nodes = input_nodes
        self.h_nodes = hidden_nodes
        self.o_nodes = output_nodes

        self.learning_rate = learning_rate

        # initialize weights (or use the given ones)
        if weights:
            self.w_input_hidden = weights[0]
            self.w_hidden_output = weights[1]
        else:
            self.w_input_hidden = np.random.rand(self.h_nodes, self.i_nodes) - 0.5
            self.w_hidden_output = np.random.rand(self.o_nodes, self.h_nodes) - 0.5
            
        print('creating NN using the following parameters:')
        print('input_nodes: ', input_nodes)
        print('hidden_nodes: ', hidden_nodes)
        print('output_nodes: ', output_nodes)
        print('learning_rate: ', learning_rate)

        self.activiation_function = lambda x : scipy.special.expit(x) # sigmoid

     
    def query(self, input_list :np.ndarray) -> np.ndarray:
        '''Uses the network to predict the output of a given input
        
        Parameters
        
            input_list :np.ndarray
                the list of input_nodes (= one image)
        
        Returns
        
            output_nodes :np.ndarray
                the list of output_nodes (= percentages for: left, right, straight)
        '''
        # input -> ann -> output
        # aufdrösseln der input_list in etwas brauchbares
        inputs = np.array(input_list, ndmin=2).T

        print(self.w_input_hidden.shape)
        print(inputs.shape)
        # X(h) = I * W(i-h)
        h_inputs = np.dot(self.w_input_hidden, inputs)
        # O(h) = sigmoid(X(h)) 
        h_outputs = self.activiation_function(h_inputs)
        # X(o) = O(h) * W(h-o)
        final_inputs = np.dot(self.w_hidden_output, h_outputs)
        # O = sigmoid(X(o))
        final_outputs = self.activiation_function(final_inputs)
        return final_outputs
    
    def debug_net(self):
        '''prints all the weights of the network'''
        
        print('w_input_hidden')
        print(self.w_input_hidden)
        print('w_hidden_output')
        print(self.w_hidden_output)

        pass
    
    @classmethod            
    def import_neural_net(cls, filename :str, learning_rate :float = 0.2):
        '''Imports all the weights for the NN from a given file
        Note: The learning rate is not imported.
        
        Parameters
        
            filename: str 
                The Name of the file to import the weights from (.npy)
                File-Structure: weights_input_hidden, weights_hidden_output
            learning_rate: float, optional (default=0.2)
                The learning rate of the NN
        '''
        
        
        with open(filename, 'rb') as f:
            print('importing network...')
            
            w_input_hidden = np.load(f)
            w_hidden_output = np.load(f)
            
            print('weights_input_hidden: ', w_input_hidden.shape)
            print('weights_hidden_output: ', w_hidden_output.shape)
            
            input_nodes = w_input_hidden.shape[1]
            hidden_nodes = w_hidden_output.shape[1]
            output_nodes = w_hidden_output.shape[0]
            
            nn = CustomNeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate, weights=(w_input_hidden, w_hidden_output))
            return nn



def get_training_and_test_indices(number_of_records, number_of_types=3, number_of_test_records_per_type=5):
    start = number_of_records // number_of_types
    training_indices = list(range(number_of_records))
    test_indices = [training_indices[start*i:start*i+number_of_test_records_per_type] for i in range(number_of_types)]
    test_indices = set([item for sublist in test_indices for item in sublist])
    training_indices = list(set(training_indices) - test_indices)   
    random.shuffle(training_indices)
    return training_indices, list(test_indices)
