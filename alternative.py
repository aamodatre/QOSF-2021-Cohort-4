""" QOSF - 2021 - Cohort 4 - Task 1 """
""" Alternative Solution - Limited Capcity"""
""" Aamod Atre - Sep 27 2021"""

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

def ket(qc):
    """Function to print the ket vector for any circuit"""
    print(qc.decompose().draw())
    # k = Statevector(qc)
    # print(k.data)

def create_states(ud):
    
    ud = np.array(ud)
    norm = 1/np.sqrt(len(ud))
    
    ub = [np.binary_repr(i) for i in ud]
    max_len = max(np.vectorize(len)(ub))
    ub = np.array([str(0)*(max_len-len(i))+i for i in ub])

    index_b = [np.binary_repr(i) for i in range(len(ud))]
    max_len_index = max(np.vectorize(len)(index_b))
    index_b = np.array([str(0)*(max_len_index-len(i))+i for i in index_b])

    binaries = np.array([address+data for address, data in zip(index_b, ub)])

    nqbits = len(binaries[0])

    """ All the Log2 Stuff"""
    n = max(ud)
    while np.log2(n).is_integer() == False:
        n -= 1
    nqbits_ud = int(np.log2(n)+1)

    """ New loop to determine the number of instace in the input array"""
    basis = np.array([i for i in range(2**nqbits)])
    
    # Convert to binary
    bbasis = [np.binary_repr(int(i)) for i in basis]
    max_len = max(np.vectorize(len)(bbasis))
    bbasis = np.array([str(0)*(max_len-len(i))+i for i in bbasis])

    instances = np.zeros(len(bbasis), dtype = np.int64)
    for b in range(len(bbasis)):
        if np.where(binaries == bbasis[b])[0].size != 0:
            # print(len(np.where(binaries == bbasis[b])[0]))
            instances[b] = len(np.where(binaries == bbasis[b])[0])

    """Loop to determine an index array"""

    indices = np.full(shape = len(bbasis), fill_value = "Nan", dtype='<U9')
    for j in range(len(bbasis)):
        if np.where(binaries == bbasis[j])[0].size != 0:
            if np.where(binaries == bbasis[j])[0].size == 1:
                indices[j] = np.where(binaries == bbasis[j])[0][0]
            else:
                m = ""
                for i in np.where(binaries == bbasis[j])[0]:
                    m += str(i)+str(" ")
                indices[j] = m

    y = []
    State = nt("State", "binary decimal index instances", defaults=["Nan"])
    for a, (b, c, d) in enumerate(zip(bbasis,indices, instances)):
        y.append((State(b,a, c,d)))

        """ For more insight - uncomment this"""
        # print("{}\n\n".format(y[a]))

    return y, norm, nqbits, nqbits_ud

def generate_sat(nqbits, nqbits_ud):
    
    # identify all possible number represented by n-qubits
    basis = np.array([i for i in range(2**nqbits)])
    
    # convert the basis to binary representation
    bbasis = [np.binary_repr(int(i)) for i in basis]
    max_len = max(np.vectorize(len)(bbasis))
    bbasis = np.array([str(0)*(max_len-len(i))+i for i in bbasis])

    # identify all possible solution states
    max_int = 2**nqbits_ud -1
    N = bin(max_int)[2:]
    
    if nqbits_ud%2 != 0:
        solA = 0
        for i in range(0,nqbits_ud,2):
            solA += int(np.binary_repr(2**i))
        solB = "0"+bin(int(str(N),2) - int(str(solA),2))[2:]
    
    elif nqbits_ud%2 == 0:
        solA = ""
        temp = 0
        for i in range(0,nqbits_ud,2):
            temp += int(np.binary_repr(2**i))
        solA += "0" + str(temp)
        solB = bin(int(str(N),2) - int(str(solA),2))[2:]
    solA = str(solA)


    """creating tensored solution states"""
    nqbits_index = nqbits - nqbits_ud

    # ibasis = index-basis
    ibasis = np.array([i for i in range(2**nqbits_index)])
    # bi-basis = index basis in binary representation
    bibasis = [np.binary_repr(int(i)) for i in ibasis]
    max_len = max(np.vectorize(len)(bibasis))
    bibasis = np.array([str(0)*(max_len-len(i))+i for i in bibasis])
    bibasis = [solA+b[::-1] for b in bibasis] + [solB+b[::-1] for b in bibasis]

    # Removing possible solutions
    bbasis = np.setdiff1d(bbasis, bibasis)


    # Generating the constraints for CNF-DIMACS file
    cnf_data = ""
    for bit in bbasis:
        stringy = ""
        for num, i, in enumerate(bit):
            if int(i)==0:
                stringy += str((num+1)*(-1))+str(" ")
            else:
                stringy += str(num+1)+str(" ")
        stringy += "0\n"
        cnf_data += stringy
    
    # number of constraints
    ncond = cnf_data.count("\n")
    with open("./dimacs-data/nnsat.dimacs", "w") as f:
        f.write("c Phase Oracle Generating DIMACS-CNF N-SAT\n")
        f.write("p cnf {} {}\n".format(nqbits, ncond))
        f.write(cnf_data)

def equal_super(qc, qr):
    """ Create Equal Superpostion"""
    for q in range(qr):
        qc.h(q)
    return qc

def search(init_circ, init_vector):
    
    """ specific quantum state initialization """
    init_circ.initialize(init_vector)

    oracle = PhaseOracle.from_dimacs_file('./dimacs-data/nnsat.dimacs')
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

#----------- START HERE -------------

if __name__ == "__main__":

    disclaimer = """\n This is NOT the main solution
                    \n***************************************
                    \n
                    \nThis alternative script can search for
                    \nsolution indices if there is only one
                    \nnumber satisfying the alternating-bit 
                    \ncondition, in binary representation.
                    \n***************************************"""
    
    print(disclaimer)

    """ Requesting User Inputs"""
    default_input = [0,2,0,3]
    user_text = """\nEnter positive numbers separated by spaces
                    \n\nCurrent Defaults : {}
                    \n(Press ENTER for defaults)
                    \n> """.format(default_input)
    user_input = [int(i) for i in input(user_text).split()] or default_input
    
    # suffix ud : user-defined decimals
    states, norm, nqbits, nqbits_ud = create_states(user_input)

    # generate the cnf-dimacs file for constraints
    generate_sat(nqbits, nqbits_ud)

    """ Initializing the circuit """
    init_vector = [np.sqrt(i.instances)*norm for i in states]
    init_state  = QuantumRegister(nqbits,"i")
    init_circ   = QuantumCircuit(init_state)
    
    cc = search(init_circ, init_vector)

    """ Sorting the counts"""
    nshotsc = np.sum([v for v in cc.values()])
    cc_probs = {k: v/nshotsc for k, v in cc.items()}
    ccmax = max(cc_probs.values())
    cc_vals = np.array([v/ccmax for v in cc_probs.values()])
    ccsorted = sorted(cc_probs.items(), key = lambda kv:(kv[1], kv[0]))
    
    """ Identifying the index """
    nqbits_index = nqbits - nqbits_ud
    index = ccsorted[-1][0][:nqbits_index]
    print("\nRequired Binary Index = {}\n".format(index))


