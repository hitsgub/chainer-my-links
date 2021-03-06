from chainer import config
from chainer import cuda
from chainer import function
import chainer.links as L

import numpy as np

from links.separable_link import SeparableLink
from models.network_templates import ResNet
from utils.utils import attention_shape


class ShakeShake(function.Function):
    """shake shake regularization."""
    def __init__(self, axes=(0, 1), a_range=(0, 1), b_range=(0, 1)):
        self.axes = axes
        self.a_range = a_range
        self.b_range = b_range
        self.E = np.mean(a_range)

    def forward(self, xs):
        x = xs[0]
        xp = cuda.get_array_module(x)
        self.retain_inputs(())
        half = x.shape[1] // 2
        if config.train:
            self.shape = attention_shape(self.axes, x.shape)
            if 1 in self.axes:
                self.shape[1] //= 2
            a = xp.random.uniform(*self.a_range, self.shape).astype(xp.float32)
            y = a * x[:, :half] + (1 - a) * x[:, half:]
        else:
            y = (x[:, :half] + x[:, half:]) * self.E
        return y,

    def backward(self, xs, gys):
        gy = gys[0]
        xp = cuda.get_array_module(gy)
        b = xp.random.uniform(*self.b_range, self.shape).astype(xp.float32)
        gx0 = gy * b
        gx1 = gy * (1 - b)
        return xp.concatenate((gx0, gx1), axis=1),


def shakeshake(x, axes=(0, 1), a_range=(0, 1), b_range=(0, 1)):
    return ShakeShake(axes, a_range, b_range)(x)


Ns = (3,) * 3
channels = (16, 32, 64)
firsts = 'CBR'
mains = 'I+BR2CBRSs'
lasts = 'BRP'
nobias = False

# Separable convolution
S = lambda _self: SeparableLink(L.Convolution2D, 1, 2, None, _self.ch, 3,
                                _self.stride, 1, nobias, _self.initialW)
# shakeshake
s = lambda _self: ShakeShake()


def model(classes):
    "Definition of 20-layer pre-activation ShakeShake ResNets."
    return ResNet(classes, Ns, channels, firsts, mains, lasts, nobias=nobias,
                  conv_keys='S', S=S, s=s)
