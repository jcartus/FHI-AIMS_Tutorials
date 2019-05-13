"""This script will plot energies.dat"""

import os
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("seaborn")

def fetch_data(folder):
    return np.loadtxt(
        fname=os.path.join(folder, "diamond", "energies.dat"),
        #delimiter=" ",
        skiprows=1
    )

def plot(data, label):
    plt.plot(data[:, 0], data[:, 1], label=label)
    plt.ylabel("Energy / eV")
    plt.xlabel("Lattice Parameter / Angstrom")
    

def main():
    
    plot(fetch_data("../Problem_01/"), "3x3x3")

    for folder in [
        "8x8x8",
        "12x12x12",
        "16x16x16"
    ]:
    
        plot(fetch_data(folder), folder)
    plt.legend()
    plt.savefig("EnergiesForGrids.png")
    plt.show()

if __name__ == '__main__':
    main()
