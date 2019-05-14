"""This script will plot energies.dat"""

import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use("seaborn")

def fetch_data(folder):
    return np.loadtxt(
        fname=os.path.join(folder, "energies.dat"),
        #delimiter=" ",
        skiprows=1
    )

def plot(data, label):

    if label == "diamond":
        data[:, 1] = data[:, 1] / 2.0

    plt.plot(data[:, 0], data[:, 1], label=label)
    plt.ylabel("Energy / eV")
    plt.xlabel("Lattice Parameter / Angstrom")
    

def main():
    
    for folder in [
        "fcc",
        "bcc",
        "diamond"
    ]:
    
        plot(fetch_data(folder), folder)
    plt.legend()
    plt.savefig("EnergiesPhases.png")
    plt.show()

if __name__ == '__main__':
    main()
