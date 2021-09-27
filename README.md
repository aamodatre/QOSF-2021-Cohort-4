# QOSF-2021
Assessment Task solution for QOSF 2021.

### Description of Problem Statement

The description of the problem is as follows:

1. Take an user-input of non-negative integers of any length into an ordered array. 
2. Using an appropriate oracle, identify the indices for numbers who have alternating 1s and 0s in their binary representation. 
3. Return an appropriate superpostion of these indices in binary representation.

### Approach and merits of the current solution

The solution presented in this repository is based on Grover's search algorithms. The solution performs two searches, one with specific quantum state initialization, and one with equal superposition initialization. The obtained counts from these searches are compared and the solution states are determined. 

_Merits of this approach_:

1. Bonus question solved - The script is able to search for appropriate solutions for any number of qubits. 

2. When only one solution number is present, and repeated 'n' times, all 'n' binary indices are accurately returned in a equal superposition

### Failures and Suggested Alternatives

The current code may fail the following cases:

1. If more than one solution state repeated. For example, the input array [1 3 1 2] will fail to identify all three solutions (2 instances of '01' and 1 instance of '10') correctly. 
2. If non-solution numbers are repeated more than once. For example, the input array [1 1 1 5] may not be able to identify the solution 5 (binary = 101).
