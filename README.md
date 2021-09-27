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

1. Bonus question regarding generalization solved. 
2. Multiple occurances of the one solution can accurately detected.

### Failures and Suggested Alternatives

The current code may fail the following cases:

1. If more than one solution state repeated. For example, the input array [1 3 1 2] will fail to identify all three solutions correctly. 
2. If non-solution numbers are repeated more than once. 
