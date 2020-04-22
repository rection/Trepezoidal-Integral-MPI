# Trepezoidal-Integral-MPI


I coded with Python2.7 and I used mpi4py. You need to follow instractures;

```
apt install mpich gcc gfortran wget python-mpi4py python-numpy -y 
mkdir $HOME/nfs
cd $HOME/nfs
wget https://bitbucket.org/mpi4py/mpi4py/downloads/mpi4py-3.0.0.tar.gz
tar -xvf mpi4py-3.0.0.tar.gz
cd $HOME/nfs/mpi4py-3.0.0
python setup.py build
python setup.py build --mpicc=/where/you/have/mpicc
python setup.py build --mpi=other_mpi
python setup.py install
```

Message Passing Interface (MPI) is a standardized and portable message-passing standard designed by a group of researchers from academia and industry to function on a wide variety of parallel computing architectures. The standard defines the syntax and semantics of a core of library routines useful to a wide range of users writing portable message-passing programs in C, C++, and Fortran. You may find more information about mpi library on this [link](https://computing.llnl.gov/tutorials/mpi/)

Aditionally, the mpi4py is a library for use MPI. You can find more information on this [link.](https://computing.llnl.gov/tutorials/mpi/)
You can run with this code.

```
git clone https://github.com/rection/Hamming-Distance-MPI
cd Hamming-Distance-MPI
mpiexec -n 4 --allow-run-as-root python2.7 Trepezoidal.py 0.0 1.0 10000
```
