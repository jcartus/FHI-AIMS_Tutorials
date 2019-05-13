"""This script will plot energies.dat"""

import numpy as np
import matplotlib.pyplot as plt

plt.style.use("seaborn")

def fetch_data():
    return np.loadtxt(
        fname="energies.dat",
        #delimiter=" ",
        skiprows=1
    )

def plot(data):
    plt.plot(data[:, 0], data[:, 1])
    plt.ylabel("Energy / eV")
    plt.xlabel("Lattice Parameter / Angstrom")
    

def main():
    plot(fetch_data())
    plt.show()

if __name__ == '__main__':
    main()
