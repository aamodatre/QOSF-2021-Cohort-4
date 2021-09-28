# QOSF-2021

This repository presents a solution for Question 1 amongst the assessments tasks for QOSF Mentorship program 2021. The script ```main.py``` presents the prescribed solution to the problem statement, by searching a generalized 1D array for the specified condition, as described below. However, in very specific cases, ```main.py``` oracle may fail to identify the right solutions. Specific drawbacks of ```main.py``` are addressed in a limited capacity with an simplified yet effective approach ```alternative.py```. Below, I've summarized the problem statement, outlining the approach of ```main.py```, and highlighted its merits and flaws. 

### Description of the Problem Statement (Q1):

The problem statement requires users to submit a 1D non-negative integer array. The script is then required to identify numbers which, in their binary representation, consist of an alternating string of 1s and 0s. The output of the script, must be an appropriate superposition of the input array indices, in a binary representation, corresponding to the numbers which satisfy this criteria.

### Approach and Merits of ```main.py``` :

This script is written in Python3, with Numpy, Qiskit and Matplotlib as dependencies. It may be executed as:
```
python3 main.py
```

The problem statement may formulated as a satisfiability problem, which is common in mathematics and computer sciences. Acknowledging that only binary numbers with alternating bits (0s and 1s) clear the specified criterion, a CNF-format DIMACS file is generated. This file comprises of the mathematical clauses that all quantum states with 'm' qubits are tested against. The CNF-DIMACS file allows the generation of an appropriate phase oracle, and Grover's diffuser operator using built-in Qiskit library functions. A subsequent Grover's search amplifies the quantum states which satisfy all clauses speficied in the DIMACS file. The outline of the algorithm is as follows. 

The solution follows the following step:
1. User-input array is stored in an ordered data-type, such as a list or tuple. 
2. The binary representations of the input array are initialized as tensored quantum states with 'm' qubits.
3. Two independent Grover's searches are conducted. One search is initilazed with an equal superpostion of all possible 'm' qubit states and the other is initialized with an equal superposition of states appearing in the user-input array.
4. The counts (or probabilities) obtained from these independently run searches are compared and solution states are conditionally determined.
5. Based on the number of solutions obtained, an appropriate superposition of indices in the binary representation is returned. 

 #### Example [5, 2, 4, 3]

- Input : [5, 2, 4, 3] &#8594; (to binary) &#8594; [101, 010, 100, 011].
- Identified solutions : [**101**, **010**, 100, 011] &#8594; (corresponding indices) &#8594; 0 and 1.
- Output : (1/sqrt(2)) * [00 + 01]

_**Merits of this approach**_:

1. Addresses the Bonus Question: The script ```main.py``` accepts vectors, with random non-negative values, of size 2^n with m bits in length for each element and finds the appropriate state(s) from an oracle.
 
2. Identifying repeated solutions: Single solutions repeated multiple times can be identified accurately.

### Flaws and suggested alternatives:

_**Flaws**_ 

After employing a variety of test cases, it is observed that ```main.py``` **may** return the incorrect indices if:

1. Numbers which do not satisfy the specified criterion are repeated more than twice. 
    - For example, in the input array [1 1 1 5], 1 is incorrectly identified as the correct solution instead of 5.

2. Multiple 'solution' numbers are repeated in the user-input array. 
    - For example, input array [1 3 1 2] contains two instances of '1' and one instance of the '2', both of which satisfy aforemention criteria, and are solutions. However, all three of these may not be correctly idenfified. 

_**Alternative**_

1. The first flaw listed above, is effectively addressed with ```alternative.py```. This script creates product state of each number index and number in the binary representation. These product states are again solved as a satisfiability problem.

- The alternative code may be executed as:
```
python3 alternative.py
```

### Resources:

This program was built solely by referencing Qiskit's documentation pages.