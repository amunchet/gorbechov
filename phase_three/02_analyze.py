#!/usr/bin/env python3
"""
Analyzes the preliminary results

NOTE: This does not run in virtualenv, due to the installation of matplotlib via apt
"""
import os
import json
import numpy as np
import matplotlib.pyplot as plt

DATA_FOLDER="./data"



def load_dataset():
    """Loads in and returns the array of data"""
    retval = []
    for fname in os.listdir(DATA_FOLDER):
        with open(os.path.join(DATA_FOLDER, fname)) as f:
            temp = json.load(f)
            retval.append((temp[-1], temp[-2]))
    return retval

def load_percentages(dataset):
    """Loads in the percentages from the dataset and returns numpy array"""
    a = [(x[1]-x[0])/x[0] for x in dataset]
    return np.array(a)

def display_graph(dataset):
    """Displays the graph"""
    plt.hist(dataset, range=(0,0.25), bins=5)
    plt.show()

if __name__ == "__main__":
    a = load_dataset()
    b = load_percentages(a)

    # I want to see some stats too
    print("Max percentage gain: ", b.max())
    print("Min percentage gain: ", b.min())
    print("Std for percentage gain: ", b.std())
    print("Mean for percentage gain: ", b.mean())

    print("% of gains over 10%: ", len([x for x in b if x > .1]))
    print("% of gains under 10%: ", len([x for x in b if x < .1]))
    print("% of gains under 5%: ", len([x for x in b if x < .05]))
    print ("Total number of inspected stocks: ", len(b))



    display_graph(b)
