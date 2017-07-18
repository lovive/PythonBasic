# -*- coding:utf-8-*-
"""
    Author: zmgao
    version: 1.0
    project name: kmeans Algorithm
    github: https://lovive.github.com/python_basic
"""

import math
import random


class Cluster(object):
    """
        clustring
    """

    def __init__(self, samples):
        if len(samples) == 0:
            # the length data size is null
            raise Exception("Error: a null data!")

        # samples in cluster
        self.samples = samples

        # sample data dimension
        self.n_dim = samples[0].n_dim

        # judge the whether the data dim is the same
        for sample in samples:
            if sample.n_dim != self.n_dim:
                raise Exception("Error: the sample of dim doesn't consistent!")
                # setting the initial clustering center

        self.centroid = self.cal_centroid()

    def __repr__(self):
        """
            return the sample
        """
        return str(self.samples)

    def update(self, samples):
        """
        calculate the centroid
        """
        old_centroid = self.centroid
        self.samples = samples
        self.centroid = self.cal_centroid()
        shift = get_distance(old_centroid, self.centroid)
        return shift

    def cal_centroid(self):
        """
        caculate the centroid for samples
        :return:
        """
        n_samples = len(self.samples)
        coords = [sample.coords for sample in self.samples]
        unzipped = zip(*coords)

        centroid_coords = [math.fsum(d_list) / n_samples for d_list in unzipped]

        return Sample(centroid_coords)


class Sample(object):
    """
        sample data
    """

    def __init__(self, coords):
        self.coords = coords  # sample data location
        self.n_dim = len(coords)  # sample data dim

    def __repr__(self):
        """
        return information
        :return:
        """
        return str(self.coords)


def get_distance(a, b):
    """
            return the Euclidean_distance of the sample
        :param b:
        :return:
     """
    if a.n_dim != b.n_dim:
        raise Exception("Error: the dim of samples different, distance can not be calculated")

    ac_diff = 0.0
    for i in range(a.n_dim):
        square_diff = pow((a.coords[i] - b.coords[i]), 2)
        ac_diff += square_diff
    distance = math.sqrt(ac_diff)

    return distance


def get_random_sample(n_dim, lower, upper):
    """
    generated random data sets
    :param n_dim:
    :param lower:
    :param upper:
    :return:
    """
    samples = Sample([random.uniform(lower, upper) for _ in range(n_dim)])
    return samples