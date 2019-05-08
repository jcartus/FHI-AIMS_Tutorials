"""This script will do the calculation and plotting required by 
Exercise 2. """

import os
import subprocess as sp
import shlex
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("seaborn")

class TemplateFiller(object):
    """'Static' class that reads the template for geometry and 
    finally fills the distances """

    template_geometry_string = None

    @classmethod
    def read_template(cls):
        with open('geometry.template', 'r') as f_template:
            cls.template_geometry_string = f_template.read()


    @classmethod
    def make_geometry_string(cls, r):
        """Creates string to be written to geometry.in"""

        if cls.template_geometry_string is None:
            cls.read_template()

        return cls.template_geometry_string.replace("Dist", str(r))




def setup_calculation_folder(r):
    """Creates a folder to the calculation of the HF molecule for a binding 
    distance r. This folder contains:
    - geometry.in for HF file, with distance Dist ->r 
    - control.in (a copy of control.tempate)
    """
    
    folder_name = str(r)

    # create folder if it does not exists
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    # create geometry.in
    with open(os.path.join(folder_name, 'geometry.in'), 'w') as f:
        f.write(TemplateFiller.make_geometry_string(r))
    
    # copy control.in
    sp.call(
        "cp control.template " + os.path.join(folder_name, "control.in"),
        shell=True
    )

    return folder_name

def execute_calculation(folder_name):
    """Cd to folder and run run.sh"""
    cmd = "cd {0}; ../run.sh; cd ..".format(shlex.quote(folder_name))
    sp.call(cmd, shell=True)

def fetch_measurement_results(folder_name):
    """Reads energy and dipolemoment from file """

    dipole, energy = False, False

    with open(os.path.join(folder_name, "output"), 'r') as f:
        for line in f.readlines():
            if 'Absolute dipole ' in line:
                dipole = float(line.split()[-3])

            if '| Total energy of the DFT / ' + \
                'Hartree-Fock s.c.f. calculation      :' in line:
                    energy = float(line.split()[-2])

            if dipole and energy:
                break

    return dipole, energy       

def plot_energies(r, energies):
    plt.plot(r, energies)
    plt.xlabel("Distance / Angstrom")
    plt.ylabel("Energy / eV")
    plt.savefig("Energies.png")

def plot_dipoles(r, dipoles):
    f = plt.figure()
    plt.plot(r, dipoles)
    plt.xlabel("Distance / Angstrom")
    plt.ylabel("Dipoles / Debye")
    plt.savefig("Dipoles.png")

def main():

    dipoles, energies = [], []
    R = [0.7, 0.8, 0.85, 0.87, 0.89, 0.91, 0.93, 0.95, 1.0, 1.1, 1.2, 1.3]
    for r in R:
        print("Processing: r = {0}".format(r))
        print(" - Setup folder")
        folder_name = setup_calculation_folder(r)
        
        print(" - Do calculation")
        execute_calculation(folder_name)

        print(" - Read results")
        results = fetch_measurement_results(folder_name)
        dipoles.append(results[0])
        energies.append(results[1])


    print("All calculations done.")

    r_min = R[np.argmin(energies)]
    print("Bond length r_{Bond} = {:2.2E}".format(r_min))

    print("Do printing")
    plot_energies(R, energies)
    plot_dipoles(R, dipoles)

    plt.show()
    



if __name__ == '__main__':
    main()