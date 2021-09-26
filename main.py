""" QOSF - 2021 - Cohort 4 - Task 1 """
""" Aamod Atre - Sep 25 2021"""

"""Inbuilt Python Imports"""
import os
import subprocess
from collections import namedtuple as nt
from pprint import pprint
os.system('clear')
subprocess.run("rm -rf __pycache__", shell = True)
if not os.path.isdir("./dimacs-data"):
    subprocess.run("mkdir ./dimacs-data", shell = True)

"""Installed Library Imports"""
import numpy as np
import matplotlib.pyplot as plt

from qiskit import Aer, transpile
from qiskit.quantum_info import Statevector
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.circuit.library import PhaseOracle
from qiskit.circuit.library import GroverOperator
from qiskit.visualization import plot_histogram

"""Local Imports"""
from cnf_generator import generate_sat

"""Required Functions"""

def ket(qc):
    """Function to print the ket vector for any circuit"""
    print(qc.decompose().draw())
    # k = Statevector(qc)
    # print(k.data)

def create_states(ud):
    """ Takes user-input in decimal basis 
        And Consolidates all relevant Data"""
    
    ud = np.array(ud)
    norm = 1/np.sqrt(len(ud))
    ub = [np.binary_repr(i) for i in ud]
    max_len = max(np.vectorize(len)(ub))
    ub = np.array([str(0)*(max_len-len(i))+i for i in ub])
    
    """ All the Log2 Stuff"""
    n = max(ud)
    while np.log2(n).is_integer() == False:
        n -= 1
    nqbits = int(np.log2(n)+1)
    # print(nqbits)
    # Previous :  int(np.log2(n))

    binaries = [np.binary_repr(i) for i in range(2**nqbits)]
    max_len = max(np.vectorize(len)(binaries))
    binaries = np.array([str(0)*(max_len-len(i))+i for i in binaries])
    
    # """Loop to determine if the number was input by the user"""
    # inputs = np.zeros(len(binaries), dtype = np.int64)
    # for j in binaries:
    #     if np.where(ub == j)[0].size != 0:
    #         inputs[np.where(binaries == j)[0][0]] = 1

    """Loop to determine an index array"""

    indices = np.full(shape = len(binaries), fill_value = "Nan", dtype='<U9')
    for j in range(len(binaries)):
        if np.where(ud == j)[0].size != 0:
            if np.where(ud == j)[0].size == 1:
                indices[j] = np.where(ud == j)[0][0]
            else:
                m = ""
                for i in np.where(ud == j)[0]:
                    m += str(i)+str(" ")
                indices[j] = m

    """ New loop to determine the number of instace in the input array"""
    instances = np.zeros(len(binaries), dtype = np.int64)
    for num in range(2**nqbits):
        if np.where(ud == num)[0].size != 0:
            instances[num] = len(np.where(ud == num)[0])
    
    y = []
    State = nt("State", "instances decimal binary index", defaults=["Nan"])
    for a, (b, c, d) in enumerate(zip(instances, binaries, indices)):
        y.append((State(b,a,c,d)))

        """ For more insight - uncomment this"""
        # print("{}\n\n".format(y[a]))

    return y, norm, nqbits

def equal_super(qc, qr):
    """ Create Equal Superpostion"""
    for q in range(qr):
        qc.h(q)
    return qc

def custom_search(init_circ, init_vector):
    """Desired Superposition""" # -  Task 1
    
    init_circ.initialize(init_vector)

    oracle = PhaseOracle.from_dimacs_file('./dimacs-data/nsat.dimacs')
    grover_operator = GroverOperator(oracle, insert_barriers = True)
    init_circ = init_circ.compose(grover_operator)
    
    init_circ.measure_all()

    sim = Aer.get_backend('aer_simulator')
    t_qc = transpile(init_circ, sim)
    counts = sim.run(t_qc, shots = 8192).result().get_counts()
    # plot_histogram(counts)
    # plt.show()
    return counts

def grover_search(init_circ, init_state):
    
    init_circ = equal_super(init_circ, init_state.size)
    oracle = PhaseOracle.from_dimacs_file('./dimacs-data/nsat.dimacs')
    grover_operator = GroverOperator(oracle, insert_barriers = True)
    init_circ = init_circ.compose(grover_operator)
    
    init_circ.measure_all()
    # ket(init_circ)

    sim = Aer.get_backend('aer_simulator')
    t_qc = transpile(init_circ, sim)
    counts = sim.run(t_qc, shots = 8192).result().get_counts()

    # plot_histogram(counts)
    # plt.show()
    return counts

def compare_counts(cc, cg):
    """ Determines the solutions"""
    nshotsc = np.sum([v for v in cc.values()])
    nshotsg = np.sum([v for v in cg.values()])
    
    # In terms of probabilities
    cc_probs = {k: v/nshotsc for k, v in cc.items()}
    cg_probs = {k: v/nshotsg for k, v in cg.items()}
    
    # Preparing the cc test
    ccmax = max(cc_probs.values())
    cc_vals = np.array([v/ccmax for v in cc_probs.values()])
    ccsorted = sorted(cc_probs.items(), key = lambda kv:(kv[1], kv[0]))

    # Preparing the cg test
    cgsorted = sorted(cg_probs.items(), key = lambda kv:(kv[1], kv[0]))
    cgmax = dict([cgsorted[-1], cgsorted[-2]])

    if np.all(cc_vals>=0.9):
        return np.array([k for k in cgmax.keys()], dtype = str)
    else:
        return np.array([k for k in dict([ccsorted[-1]]).keys()], dtype = str)


#----------------START HERE----------------------

if __name__ == "__main__":
    
    """ Requesting User Inputs"""
    default_input = [5,2,4,3]
    user_text = """\nEnter positive numbers separated by spaces
                    \n\nCurrent Defaults : {}
                    \n(Press ENTER for defaults)
                    \n> """.format(default_input)
    user_input = [int(i) for i in input(user_text).split()] or default_input
    
    """Circuit Initialization"""
    state_info, norm, nqbits = create_states(user_input)
    generate_sat(nqbits)

    init_vector = [np.sqrt(i.instances)*norm for i in state_info]
    # print(init_vector)
    init_state  = QuantumRegister(nqbits,"i")
    init_circ   = QuantumCircuit(init_state)
    init_circ_grover = init_circ.copy()
    
    """ Obtaining Counts from two different searches """
    cc = custom_search(init_circ, init_vector)
    cg = grover_search(init_circ_grover, init_state)
    
    """ Determining Solutions based on Counts """
    sol = compare_counts(cc, cg)

    """Printing Output Indices"""
    indices = []
    for i in range(len(state_info)):
        if state_info[i].binary in sol:
            indices.append(state_info[i].index)

    # Convert to binary
    # print(indices)
    if len(indices) == 1:
        indices = indices[0].split()
    
    if "Nan" in indices[0]:
        raise ValueError (" No Solution in Input Array")

    indices = [np.binary_repr(int(i)) for i in indices]
    max_len = max(np.vectorize(len)(indices))
    if max_len == 1:
        max_len = 2
    indices = np.array([str(0)*(max_len-len(i))+i for i in indices])

    print("Required Binary Index Superposition = {}*[1/sqrt({})]".format(indices, len(indices)))