"""This script plots the hydrogen energies with different basis sets. """

import numpy as np
import matplotlib.pyplot as plt

plt.style.use("seaborn")

def fetch_data():
    return np.loadtxt(
        fname="energies.csv",
        delimiter=";",
        skiprows=1
    )

def plot(data):
    plt.plot(data[:, 0], data[:, 1])
    plt.ylabel("Energy / eV")
    plt.xlabel("Basis Size / arb.")
    plt.xticks(
        ticks=list(range(4)),
        labels=['Minimal', 'Tier1', 'Tier 2', 'Tier 3']
    )

def main():
    plot(fetch_data())
    plt.show()

if __name__ == '__main__':
    main()
