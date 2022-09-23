import pytest
import subprocess
import os

def test_link(fc='gfortran', file='test'):
    """ 
    Test to check that generated FORTRAN object can be linked with the TF-fortran library
    """ 
    # May be specfic to my system
    subprocess.run(["export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/.local/lib"], shell=True)
    ret = subprocess.run([fc, "-c", "-I", "../../src", f'../{file}_script.F90'])
    assert ret.returncode == 0
    ret = subprocess.run([fc, "-I", "../../src/", f"{file}_script.o", f"../{file}.o",\
        "../../src/libfortran_tensorflow.a", "-L", "/home/is500/.local/lib/", \
        "-ltensorflow", "-o", f"../{file}_script"])
    assert ret.returncode == 0
    os.remove(f"{file}_script.o")