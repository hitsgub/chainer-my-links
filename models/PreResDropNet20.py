from functions.shake_drop import ShakeDrop
from models.network_templates import ResNet

Ns = (3,) * 3
channels = (16, 32, 64)
firsts = 'CBR'
mains = 'I+BRCBRCS'
lasts = 'BRP'
nobias = False


def S(_self):
    return ShakeDrop(_self.depth_rate, a_range=(0, 0), b_range=(0, 0))


def model(classes):
    "Definition of 20-layer pre-activation stochastic ResNets."
    return ResNet(classes, Ns, channels, firsts, mains, lasts, nobias=nobias,
                  S=S)
