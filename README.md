# QOSF-2021

This repository presents a solution for Question 1 amongst the assessments tasks for QOSF Mentorship program 2021. The primary solution ```main.py``` presents a complete solution to the problem statement, searching a generalized 1D array for the specified condition, described below. However, in very specific cases, ```main.py``` may fail to identify the right solutions. Specific drawbacks of ```main.py``` are addressed in a limited capacity with an simplified yet effective approach ```alternative.py```. Below, I've summarized the problem statement, outlining the approach of ```main.py```, and highlighted its merits and flaws. 

### Description of the Problem Statement (Q1):

The problem statement requires users to submit a 1D non-negative integer array. The script is then required to identify numbers which, in their binary representation, consist of an alternating string of 1s and 0s. The output of the script, must be an appropriate superposition of the input array indices, in a binary representation, of the numbers which satisfy this criteria.

### Approach and Merits of ```main.py``` :

This script is written in Python3, with Numpy, Qiskit and Matplotlib as dependencies. It may be executed as:
```
python3 main.py
```
The problem statement may formulated as a satisfiability problem, which is common in mathematics and computer sciences. Acknowledging that only number with alternating bits clear the speficied criterion, a CNF-format DIMACS file is generated. This file comprises of the clauses that quantum states need to satisfy. The CNF-DIMACS file allows the generation of an appropriate phase oracle, and Grover's diffuser operator. The outline of the algorithm is as follows. 

The solution follows the following step:
1. User-input array is stored in an ordered data-type, such as a list or tuple. 
2. The numbers, in their binary representation, are initialized as tensored quantum states with 'n' qubits.
3. Two independent Grover's searches are run, one initilazed with an equal superpostion of all possible states and another with an equal superposition of states appearing in the user-input array.
4. The counts (or probabilites) obtained from these independent searches are compared and solution states are conditionally determined. 
5. Based on the number of solutions obtained, an appropriate superposition of indices in the binary representation is returned. 

 #### Example [5, 2, 4, 3]

- Input : [5, 2, 4, 3] &#8594; (to binary) &#8594; [101, 010, 100, 011].
- Idenfied solutions : [**101**, **010**, 100, 011] &#8594; (identified indices) &#8594; 0 and 1.
- Output : (1/sqrt(2)) * [ket(00) + ket(01)]


_**Merits of this approach**_:

1. Addresses the Bonus Question: The script accepts vectors with random values of size 2^n with m bits in length for each element and finds the appropriate state(s) from an oracle.
 
2. Identifying repeated solutions: Single solutions repeated multiple times are identified accurately.

### Flaws and suggested alternatives:

_**Flaws**_ 

After employing a variety of test cases, it is observed that ```main.py``` **may** return the incorrect indices if:

1. Numbers which do not satisfy the specified criterion are repeated more than twice. For e.g. in the input array [1 1 1 5], 1 is incorrectly identified as the correct solution.

2. Multiple 'solution' numbers are repeated several times. For e.g. [1 3 1 2] contains two instances of the solution '1' and one instance of the solution '2'. However, all three of these may not be correctly idenfified. 

_**Alternative**_

1. The first flaw listed above, is effectively solved with ```alternative.py```. This script creates product state of each number index and number in the binary representation. These product states are again solved as a satisfiability problem.

- The alternative code may be executed as:
```
python3 alternative.py
```

### Resources:

This program was built solely by referencing Qiskit's documentation pages.