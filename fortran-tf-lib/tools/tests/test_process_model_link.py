import pytest
import subprocess
import os

@pytest.fixture
def tf_lib():
    return subprocess.run(["make", "-C", "../src"], check=True)

@pytest.fixture
def my_model(tf_lib):
	subprocess.run(["process_model", "../my_model/", "-o", "testf.f90"])
	subprocess.run(["gfortran", "-c", "-I", "../src/", "testf.f90"], check=True)

def test_link(my_model, fc='gfortran', file='test'):
    """ 
    Test to check that generated FORTRAN object can be linked with the TF-fortran library
    """ 
    # May be specfic to my system
    # subprocess.run(["export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/.local/lib"], shell=True)
    ret = subprocess.run([fc, "-c", "-I", "../src", f'{file}_script.F90'])
    assert ret.returncode == 0
    ret = subprocess.run([fc, "-I", "../src/", f"{file}_script.o", f"{file}.o",\
        "../src/libfortran_tensorflow.a", \
        "-ltensorflow", "-o", f"{file}_script"])
    assert ret.returncode == 0
    os.remove(f"{file}_script.o")