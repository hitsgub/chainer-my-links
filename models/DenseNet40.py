from models.network_templates import DenseNet

Ns = (12,) * 3
first_channels = 16
channels = 12
firsts = 'CBR'
mains = 'I,BRC'
lasts = 'BRP'
keys_join = 'BRcA'
trans_theta = 1
nobias = True


def model(classes):
    "Definition of 40-layer DenseNets."
    return DenseNet(classes, Ns, first_channels, channels, firsts, mains,
                    lasts, keys_join, trans_theta, nobias=nobias)
