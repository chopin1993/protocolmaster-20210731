import matplotlib.pyplot as plt

# coding=utf-8
from matplotlib import pyplot as plt

def show_data(X):
    fig = plt.figure()
    ax = fig.add_subplot(231)
    ax.imshow(X)

    ax = fig.add_subplot(232)
    im = ax.imshow(X, cmap=plt.cm.gray,interpolation='nearest',vmin=0,vmax=255)  # 灰度
    fig.colorbar(im,shrink=0.5)

    ax = fig.add_subplot(233)
    im = ax.imshow(X, cmap=plt.cm.spring)  # 春
    plt.colorbar(im)

    ax = fig.add_subplot(234)
    im = ax.imshow(X, cmap=plt.cm.summer)
    plt.colorbar(im, cax=None, ax=None, shrink=0.5)  # 长度为半

    ax = fig.add_subplot(235)
    im = ax.imshow(X, cmap=plt.cm.autumn)
    plt.colorbar(im, shrink=0.5, ticks=[-1, 0, 1])

    ax = fig.add_subplot(236)
    im = ax.imshow(X, cmap=plt.cm.winter)
    plt.colorbar(im, shrink=0.5)


X = [[5, 6], [7, 8]]
show_data(X)
plt.show()