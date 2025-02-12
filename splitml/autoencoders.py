"""
Autoencoders for signal denoising

Author: Amber Day
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from complexPyTorch.complexLayers import ComplexLinear
from splitml.activations import complex_phase_tanh

class ComplexNet(nn.Module):
    """
    Autoencoder which operates with complex data and complex activations/losses
    """
    def __init__(self, t_input, activation, M=10, H=5): 
        
        # t_input: len(t) where t is time point vector
        # activation: desired activation function
        # M: output size of linear layer
        # H: output size of hidden layer
        
        super(ComplexNet, self).__init__()
        self.transform_lin_layer = ComplexLinear(t_input, M) 
        self.transform_hidden_layer = ComplexLinear(M, H)
        self.inverse_hidden_layer = ComplexLinear(H, M)
        self.inverse_lin_layer = ComplexLinear(M, t_input)
        self.activation = activation 
        
    def forward(self, t): 
        m = self.activation(self.transform_lin_layer(t))
        h = self.activation(self.transform_hidden_layer(m))
        m = self.activation(self.inverse_hidden_layer(h))
        t = self.inverse_lin_layer(m)
        
        return t

    def embed(self, t): 
        m = self.activation(self.transform_lin_layer(t))
        h = self.activation(self.transform_hidden_layer(m))
        
        return h


class DualRealNet(nn.Module):
    """
    Autoencoder which operates separately on real and imaginary data using real activations/losses
    """
    def __init__(self, t_input, activation, M=10, H=5): 
        
        # t_input: len(t) where t is time point vector
        # activation: desired activation function
        # M: output size of linear layer
        # H: output size of hidden layer
        
        super(DualRealNet, self).__init__()
        self.transform_lin_layer = nn.Linear(t_input, M) 
        self.transform_hidden_layer = nn.Linear(M, H)
        self.inverse_hidden_layer = nn.Linear(H, M)
        self.inverse_lin_layer = nn.Linear(M, t_input)
        
        self.activation = activation
        
    def forward(self, t): 
        m = self.activation(self.transform_lin_layer(t))
        h = self.activation(self.transform_hidden_layer(m))
        m = self.activation(self.inverse_hidden_layer(h))
        t = self.inverse_lin_layer(m)
        
        return t

    def embed(self, t): 
        m = self.activation(self.transform_lin_layer(t))
        h = self.activation(self.transform_hidden_layer(m))
        
        return h
