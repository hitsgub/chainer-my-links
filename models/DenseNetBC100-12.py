from models.network_templates import DenseNet

Ns = (16,) * 3
channels = 12
first_channels = channels * 2
firsts = 'CBR'
mains = 'I,BR4cBRC'
lasts = 'BRP'
keys_join = 'BRcA'
trans_theta = 0.5
nobias = True


def model(classes):
    "Definition of 100-layer DenseNets."
    return DenseNet(classes, Ns, first_channels, channels, firsts, mains,
                    lasts, keys_join, trans_theta, nobias=nobias)
