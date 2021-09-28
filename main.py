""" QOSF - 2021 - Cohort 4 - Task 1 """
""" Aamod Atre - Sep 25 2021"""

"""Inbuilt Python Imports"""
import os
import subprocess
from collections import namedtuple as nt
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

"""Required Functions"""

def ket(qc):
    """Function to print the ket and detailed Qiskit circuit"""
    print(qc.decompose().draw())
    # k = Statevector(qc)
    # print(k.data)

def create_states(ud):
    """ Takes user-input in decimal basis 
        And consolidates all relevant date:
        such as decimal and binary representations, 
        number of instances and indices"""
    
    # ud : user-defined decimals
    ud = np.array(ud)
    norm = 1/np.sqrt(len(ud))
    
    # ub : user-defined binary representations
    ub = [np.binary_repr(i) for i in ud]
    max_len = max(np.vectorize(len)(ub))
    ub = np.array([str(0)*(max_len-len(i))+i for i in ub])
    
    """ Determining number of qubits"""
    n = max(ud)
    while np.log2(n).is_integer() == False:
        n -= 1
    nqbits = int(np.log2(n)+1)
    
    """ Determing all possible binary number represented by n-qubits"""
    binaries = [np.binary_repr(i) for i in range(2**nqbits)]
    max_len = max(np.vectorize(len)(binaries))
    binaries = np.array([str(0)*(max_len-len(i))+i for i in binaries])
    
    """Loop to determine indices in the user-input array"""
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

    """ Loop to determine the number of instances in the user-input array"""
    instances = np.zeros(len(binaries), dtype = np.int64)
    for num in range(2**nqbits):
        if np.where(ud == num)[0].size != 0:
            instances[num] = len(np.where(ud == num)[0])
    
    """Consolidation"""
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
    
    """ specific quantum state initialization """
    init_circ.initialize(init_vector)

    oracle = PhaseOracle.from_dimacs_file('./dimacs-data/nsat.dimacs')
    grover_operator = GroverOperator(oracle, insert_barriers = True)
    init_circ = init_circ.compose(grover_operator)
    
    init_circ.measure_all()

    """ circuit simulation """
    sim = Aer.get_backend('aer_simulator')
    t_qc = transpile(init_circ, sim)
    counts = sim.run(t_qc, shots = 8192).result().get_counts()
    # plot_histogram(counts)
    # plt.show()
    return counts

def grover_search(init_circ, init_state):
    
    """ initialization with equal superposition of all states """

    init_circ = equal_super(init_circ, init_state.size)
    oracle = PhaseOracle.from_dimacs_file('./dimacs-data/nsat.dimacs')
    grover_operator = GroverOperator(oracle, insert_barriers = True)
    init_circ = init_circ.compose(grover_operator)
    
    init_circ.measure_all()
    # ket(init_circ)

    """ simulating the circuit """
    sim = Aer.get_backend('aer_simulator')
    t_qc = transpile(init_circ, sim)
    counts = sim.run(t_qc, shots = 8192).result().get_counts()

    # plot_histogram(counts)
    # plt.show()
    return counts

def compare_counts(cc, cg):
    """ Determining the solutions 
        based on counts obtained from 
        independently run circuits """

    # Total number of runs per circuit
    nshotsc = np.sum([v for v in cc.values()])
    nshotsg = np.sum([v for v in cg.values()])
    
    # Counts in terms of probabilities
    cc_probs = {k: v/nshotsc for k, v in cc.items()}
    cg_probs = {k: v/nshotsg for k, v in cg.items()}
    
    # determin highest counts by custom search
    ccmax = max(cc_probs.values())
    cc_vals = np.array([v/ccmax for v in cc_probs.values()])
    ccsorted = sorted(cc_probs.items(), key = lambda kv:(kv[1], kv[0]))

    # determine highest counts by grover's search
    cgsorted = sorted(cg_probs.items(), key = lambda kv:(kv[1], kv[0]))
    cgmax = dict([cgsorted[-1], cgsorted[-2]])

    # grover's search finds two solutions accurately, 
    # while the custom search identifies odd number 
    # of solutions with greater accuracy. 
    #
    #  This leads to the following condition:

    if np.all(cc_vals>=0.9):
        return np.array([k for k in cgmax.keys()], dtype = str)
    else:
        return np.array([k for k in dict([ccsorted[-1]]).keys()], dtype = str)

def generate_sat(size):
    """ Function to generate a DIMACS-CNF file
        and treat the search as a satisfiability
        problem """
    
    nqbits = size

    # Basis array of all possible solutions
    basis = np.array([i for i in range(2**nqbits)])

    # converting this basis to binary (bbasis)
    bbasis = [np.binary_repr(int(i)) for i in basis]
    max_len = max(np.vectorize(len)(bbasis))
    bbasis = np.array([str(0)*(max_len-len(i))+i for i in bbasis])
    
    # creating possible solution states from the number of qubits
    max_int = 2**nqbits -1
    N = bin(max_int)[2:]
    
    if size%2 != 0:
        solA = 0
        for i in range(0,nqbits,2):
            solA += int(np.binary_repr(2**i))
        solB = "0"+bin(int(str(N),2) - int(str(solA),2))[2:]
    
    elif size%2 == 0:
        solA = ""
        temp = 0
        for i in range(0,nqbits,2):
            temp += int(np.binary_repr(2**i))
        solA += "0" + str(temp)
        solB = bin(int(str(N),2) - int(str(solA),2))[2:]

    # exclude all possible solutions from binary-basis
    # The remaining basis is subjected to constraints

    solA = str(solA)
    sols = np.array((solA, solB))
    bbasis = np.setdiff1d(bbasis, sols)
    
    cnf_data = ""
    for bit in bbasis:
        stringy = ""
        for num, i, in enumerate(bit):
            if int(i)>0:
                stringy += str((num+1)*(-1))+str(" ")
            else:
                stringy += str(num+1)+str(" ")
        stringy += "0\n"
        cnf_data += stringy

    # write to file
    with open("./dimacs-data/nsat.dimacs", "w") as f:
        f.write("c Phase Oracle Generating DIMACS-CNF N-SAT\n")
        f.write("p cnf {} {}\n".format(nqbits, 2**nqbits-2))
        f.write(cnf_data)

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

    # init_vector initializes states based on their
    # occurance in the decimal representation of the input array
    init_vector = [np.sqrt(i.instances)*norm for i in state_info]
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