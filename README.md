# QOSF-2021
Assessment Task solution for QOSF 2021.

This repository presents two solutions for Question 1 amongst the assessments tasks for QOSF Mentorship program 2021. The primary solution (_main.py_) presents a complete solution to the problem statement, searching a generalized 1D array for the specified condition, described below. However, in very specific cases, _main.py_ may fail to identify the right solutions, and for these reason, a more elegant approach (_alternative.py_) is presented. This alternative, however, currently identifies only succeeds in arrays with single solutions, and therefore should only be used in this capacity. Below, I've summarized the problem statement, outlines the approach of _main.py_, and highlighted some merits and flaws. 

### Description of the Problem Statement (Q1):

The problem statement requires users to submit a 1D non-negative integer array. The script is then required to identify numbers which, in their binary representation, consist of an alternating string of 1s and 0s. The output of the script, must be an appropriate superposition of the input array indices, in a binary representation, of the numbers which satisfy this criteria.

### Approach and Merits of _main.py_ :

This script is written in Python3, with Numpy, Qiskit and Matplotlib as dependencies. It may be executed as:
```
python3 main.py
```

The solution follows the following step:
1. User-input array is stored in an ordered data-type, such as a list or tuple. 
2. The numbers, in their binary representation, are initialized as tensored quantum states with 'n' qubits.
3. Two independent Grover's searches are run, one initilazed with an equal superpostion of all possible states and another with an equal superposition of states appearing in the user-input array.
4. The counts (or probabilites) obtained from these independent searches are compared and solution states are conditionally determined. 
5. Based on the number of solutions obtained, an appropriate superposition of indices in the binary representation is returned. 

 #### Example [5, 2, , 3]

<span style="color: red;">text</span>
_Merits of this approach_:

1. Bonus question solved - The script is able to search for appropriate solutions for any number of qubits. 

2. When only one solution number is present, and repeated 'n' times, all 'n' binary indices are accurately returned in a equal superposition

### Failures and Suggested Alternatives

The current code may fail the following cases:

1. If more than one solution state repeated. For example, the input array [1 3 1 2] will fail to identify all three solutions (2 instances of '01' and 1 instance of '10') correctly. 
2. If non-solution numbers are repeated more than once. For example, the input array [1 1 1 5] may not be able to identify the solution 5 (binary = 101).

### Resources:

This program was built solely by referencing Qiskit's documentation pages.