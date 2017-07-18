# -*- coding:utf-8-*-
"""
    Author: zmgao
    version: 1.0
    project name: kmeans Algorithm
    github: https://lovive.github.com/python_basic
"""

import random
from kmeans_tools import Cluster, get_distance,get_random_sample
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors

def kmeans(samples, k, cutoff):
    """
    the function of kmeans
    """
    # first ramdon choose k samples
    init_samples = random.sample(samples,k)

    # construct k clustering, and the initial random sample as centroid
    clusters = [Cluster([sample]) for sample in init_samples]

    # iterate untill reach steady state
    n_loop = 0
    while True:
        lists = [[] for _ in clusters]

        # starts
        n_loop += 1
        for sample in samples:
            smallest_distance = get_distance(sample,clusters[0].centroid)
            cluster_index = 0

            for i in range(k-1):
                distance = get_distance(sample,clusters[i+1].centroid)
                if distance < smallest_distance:
                    smallest_distance = distance
                    cluster_index = i+1

             # find the centroid and update the cluster
            lists[cluster_index].append(sample)

        # initial the shift max distance
            biggest_shift = 0.0

        for i in range(k):
            shift = clusters[i].update(lists[i])
            # record the biggest shift distance
            biggest_shift = max(biggest_shift,shift)

        # if the shift distance is smaller than cutoff, the clustering stable
            if biggest_shift < cutoff:
                print("{} iterate, stable.".format(n_loop))
                break

        return clusters

def run_main():
    """
    main function
    :return:
    """
    # sample number
    n_samples = 1000

    # sample features
    n_feat = 2

    # feature range
    lower = 0
    upper = 200

    # cluster number
    n_cluster = 5

    # random generated the sample data
    samples = [get_random_sample(n_feat,lower,upper) for _ in range(n_samples)]

    # the stable cut off
    cutoff = 0.2

    # use the kmeans methods
    clusters = kmeans(samples, n_cluster, cutoff)

    # print the results
    for i, c in enumerate(clusters):
        for sample in c.samples:
            print("cluster--{},sample--{}".format(i,sample))

    # plot the results
    plt.subplot()
    color_names = list(mcolors.cnames)
    for i,c in enumerate(clusters):
        x = []
        y = []
        random.choice
        color = [color_names[i]]*len(c.samples)
        for sample in c.samples:
            x.append(sample.coords[0])
            y.append(sample.coords[1])
        plt.scatter(x,y,c=color)
    plt.show()

if __name__ == '__main__':
    run_main()
