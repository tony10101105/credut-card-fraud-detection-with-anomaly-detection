import os
import torch
import torchvision
import torch.nn as nn
from torch.autograd import Variable
from torchvision import datasets, transforms

torch.manual_seed(0)#for reproducibility

def weights_init_normal(m):
    classname = m.__class__.__name__
    if classname.find('Conv') != -1:
        nn.init.xavier_uniform_(m.weight.data)
    elif classname.find('Linear') != -1:
        nn.init.normal_(m.weight.data)
        nn.init.constant_(m.bias.data, 0.0)
    elif classname.find('BatchNorm1d') != -1:
        nn.init.normal_(m.weight.data)
        nn.init.constant_(m.bias.data, 0.0)
        
def init_weights(net_layer):
    try:
        net_layer.apply(weights_init_normal)
    except:
        raise NotImplementedError('weights initialization error')


class FCNN(nn.Module):#discriminator
    def __init__(self):
        super(FCNN, self).__init__()
        self.layer = nn.Sequential(nn.Linear(30, 10),
                                    nn.BatchNorm1d(10),
                                    nn.ReLU(True),
                                    nn.Linear(10, 1))
        init_weights(self.layer)
        
        self.sigmoid = nn.Sigmoid()
        
    def forward(self, x):
        x = self.layer(x)
        x = self.sigmoid(x)
        return x

class autoencoder(nn.Module):#generator
    def __init__(self):
        super(autoencoder, self).__init__()
        self.encoder = nn.Sequential(nn.Linear(30, 15),
                                     #nn.BatchNorm1d(15),
                                     nn.ReLU(True),
                                     nn.Linear(15, 8),
                                     #nn.BatchNorm1d(8),
                                     nn.ReLU(True))
        init_weights(self.encoder)
        
        self.decoder = nn.Sequential(nn.Linear(8, 15),
                                     #nn.BatchNorm1d(15),
                                     nn.ReLU(True),
                                     nn.Linear(15, 30))
        init_weights(self.decoder)
        
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        x = self.sigmoid(x)
        return x
        

    


    
