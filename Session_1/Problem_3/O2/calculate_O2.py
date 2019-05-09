""" This file will calculate the binding curve for various methods and spin 
configurations.
"""

import os
import subprocess as sp
import shutil
import shlex
import numpy as np
import matplotlib.pyplot as plt

plt.style.use("seaborn")

class TemplateFiller(object):
    """'Static' class that reads the template for geometry and 
    finally fills the distances """

    template_geometry = None
    template_control = None

    spin_treatment = {
        'default': "\n",
        'collinear': "spin collinear " + os.linesep + \
            "default_initial_moment 2.0"
    }

    @classmethod
    def read_template(cls, name):
        with open(name +'.template', 'r') as f_template:
            if name == 'geometry':
                cls.template_geometry = f_template.read()
            elif name == 'control':
                cls.template_control = f_template.read()   
            else:
                raise ValueError("Unknown template: " + name)


    @classmethod
    def make_geometry_string(cls, r):
        """Creates string to be written to geometry.in"""

        if cls.template_geometry is None:
            cls.read_template('geometry')

        return cls.template_geometry.replace("Dist", str(r))


    @classmethod
    def make_control_string(cls, method, spin):
        """Creates string to be written to geometry.in"""

        if cls.template_control is None:
            cls.read_template('control')

        control_string = cls.template_control
        control_string = \
            control_string.replace("SPIN", cls.spin_treatment[spin])
        control_string = \
            control_string.replace("METHOD", method)

        return control_string

def setup_calculation_folder(r, method, spin):
    """Creates a folder to the calculation of the HF molecule for a binding 
    distance r. This folder contains:
    - geometry.in for HF file, with distance Dist ->r 
    - control.in (a copy of control.tempate)
    """
    
    folder_name = spin + "_" + method + "_" + str(r)

    # create folder if it does not exists
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name, ignore_errors=True)
    
    os.mkdir(folder_name)

    # create geometry.in
    with open(os.path.join(folder_name, 'geometry.in'), 'w') as f:
        f.write(TemplateFiller.make_geometry_string(r))
    
    # create geometry.in
    with open(os.path.join(folder_name, 'control.in'), 'w') as f:
        f.write(TemplateFiller.make_control_string(method, spin))

    return folder_name

def execute_calculation(folder_name):
    """Cd to folder and run run.sh"""
    cmd = "cd {0}; ../run.sh; cd ..".format(shlex.quote(folder_name))
    sp.call(cmd, shell=True)

def fetch_measurement_results(folder_name):
    """Reads energy and dipolemoment from file """

    energy = False

    with open(os.path.join(folder_name, "output"), 'r') as f:
        for line in f.readlines():
            
            if '| Total energy of the DFT / ' + \
                'Hartree-Fock s.c.f. calculation      :' in line:
                    
                    energy = float(line.split()[-2])
                    break

        if not energy:
            raise RuntimeError("No energy found!")

    return energy       

def main():

    R = np.arange(0.8, 1.7, 0.1)

    plt.figure()

    for spin in ['default', 'collinear']:

        print("Start spin treatment: " + spin)

        for method in ['pbe', 'pbe0']:

            print(" - Start method: " + method)

            energies = []

            for r in R:
                print("    - Processing: r = {0}".format(r))
                print("       - Setup folder")
                folder_name = setup_calculation_folder(r, method, spin)
                
                print("       - Do calculation")
                execute_calculation(folder_name)

                print("       - Read results")
                energies.append(fetch_measurement_results(folder_name))

            print(" - Calculations done.")

            r_min = R[np.argmin(energies)]
            print(" - Bond length r_0 = {:1.5E}".format(r_min))

            print(" - plot bonding curve")
            plt.plot(R, energies, label=spin + " & " + method)

    print("All calculations done.")


    plt.legend()
    plt.ylabel("Energy / eV")
    plt.xlabel("Bonding distance / Angstrom")
    plt.title("O2 Bonding potential for different methods/Spin treatments")

    plt.savefig("BondPotentialO2.png")

    plt.show()

if __name__ == '__main__':
    main()