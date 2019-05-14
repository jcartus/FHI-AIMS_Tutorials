#!/usr/bin/python
import os
import shutil
import numpy as np

#-------------------------------------------------------------
#-------------Change script here------------------------------
#-------------------------------------------------------------

os.system("source ../../../Session_1/export_aims_metadata.sh")
os.system("echo $fhi_aims")

# Enter your calculated value for the minimal lattice constant 
aMin = 5.1
# Enter your calculated value for the maximal lattice constant
aMax = 5.7
# Enter a value for the stepwidth
step = 0.1
# Number of calculations
n = int(np.rint((aMax - aMin)/step)) + 1

vector = np.zeros([3,3])
# Lattice vector in units of the lattice constant
vector[0] = [0.0,0.5,0.5]
vector[1] = [0.5,0.0,0.5]
vector[2] = [0.5,0.5,0.0]

#Number of basis atoms
atom_no = 2

atoms = np.zeros([atom_no,3])

#Basis atoms in fractional coordinates
atoms[0] = [0.0,0.0,0.0]
atoms[1] = [0.25,0.25,0.25]

#-------------------------------------------------------------
#-------------End change script here--------------------------
#-------------------------------------------------------------

for i in range(n):
   aLat = aMin + step * i
   print("Processing lattice constant %10.6f AA." % aLat)
   # Create directory
   dirname = str(aLat)
   if not os.path.exists(dirname):
     os.makedirs(dirname)
   # Change to directory        
   os.chdir(dirname)
   lattice_vector = vector * aLat
   # Write geometry.in
   filename = "geometry.in"
   f = open(filename,'w')
   # The lattice
   for lat in lattice_vector :
	f.write("lattice_vector {:10.6f} {:10.6f} {:10.6f}\n".format(lat[0],lat[1],lat[2])) 
   # The atoms
   for a in atoms:
   	f.write("atom_frac {:10.6f} {:10.6f} {:10.6f} Si\n".format(a[0],a[1],a[2]))
   # Close file
   f.close()

   # Copy the control file
   shutil.copyfile("../control.in","control.in")

   # Run FHI-aims on 4 processes
   #os.system("mpirun -n 4 aims.x > aims.out")
   os.system("$fhi_aims > aims.out")

   # Change back to former directory
   os.chdir("..")
