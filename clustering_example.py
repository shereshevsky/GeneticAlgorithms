from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pandas as pd

from data.emr3d1 import get_emr3d1

EMR3d1, variables1 = get_emr3d1()

y_pred_KMeans1 = KMeans(n_clusters=3).fit_predict(EMR3d1)


def make_chart(chart_data, y_pred, labels):
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    ax.set_zlabel(labels[2])
    ax.scatter(chart_data[:, 0], chart_data[:, 1], chart_data[:, 2], c=y_pred)
    plt.show()


if __name__ == '__main__':
    make_chart(EMR3d1, y_pred_KMeans1, variables1)

