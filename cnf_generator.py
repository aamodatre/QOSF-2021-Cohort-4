""" File made out of frustration """

import numpy as np
from pprint import pprint

def generate_sat(size):
    
    nqbits = size
    # Array of all solutions
    basis = np.array([i for i in range(2**nqbits)])

    # Convert to binary
    bbasis = [np.binary_repr(int(i)) for i in basis]
    max_len = max(np.vectorize(len)(bbasis))
    bbasis = np.array([str(0)*(max_len-len(i))+i for i in bbasis])
    
    # creating possible solutions
    max_int = 2**nqbits -1
    N = bin(max_int)[2:]
    # print(N)
    
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

    # Removing possible solutions
    solA = str(solA)
    sols = np.array((solA, solB))
    # from pprint import pprint
    # pprint(sols)
    bbasis = np.setdiff1d(bbasis, sols)


    # Create an array (boy) - from 0 to 2**qbits - Convert to binary
    # Create solution states?
    # By adding powers of two alternatively. 
    # substract from 2**N
    # Remove these two solution states. 

    # Now convert this to DIMACS. 
    # Array of length qbits 
    # range from 1 to qbits-1
    
    # newarr = [i for i in range(1,nqbits)]
    
    # Take this array and 
    # implement a - sign according to the element in the first array (boy)
    # Multiply by -1 in list newarr if bit greater than 0
    # Then add to string
    
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

    with open("./dimacs-data/nsat.dimacs", "w") as f:
        f.write("c Phase Oracle Generating DIMACS-CNF N-SAT\n")
        f.write("p cnf {} {}\n".format(nqbits, 2**nqbits-2))
        f.write(cnf_data)

    # Hmmm... new stuff. 
    # take modulo (//2) and right shift? Okay. 
    # Append this stuff into a string (with the line endings too.)
    # Write this string directly?


    
if __name__ == "__main__":
    raise RuntimeError ("Kindly execute the file Q1-Aamod.py")