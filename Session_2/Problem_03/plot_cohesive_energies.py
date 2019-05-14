"""This script will plot energies.dat"""

import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use("seaborn")

def fetch_data(folder):
    return np.loadtxt(
        fname=os.path.join(folder, "cohesive.dat"),
        #delimiter=" ",
        skiprows=1
    )

def plot(data, label):

    plt.plot(data[:, 0], data[:, 1], label=label)
    plt.ylabel("Energy / eV")
    plt.xlabel("Volume Per Atom / Angstrom")
    

def main():
    
    for folder in [
        "fcc",
        "bcc",
        "diamond"
    ]:
    
        plot(fetch_data(folder), folder)

    plt.legend()
    plt.savefig("EnergiesCohesivePhases.png")
    plt.show()

if __name__ == '__main__':
    main()
