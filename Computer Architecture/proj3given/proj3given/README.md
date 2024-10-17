# Project 3 README

Student 1: Full Name 1 (123456789)
Student 2: Full Name 2 (123456798)

## Project Status
This the current status of the project ...

## Known Issues
The project fails to function properly in ...

## References
* [Build an XOR gate from AND/NOT](https://electronics.stackexchange.com/questions/487529/build-an-xor-gate-from-and-not)
* [Some other link](https://stackoverflow.com)

## Generative AI Use
I used ChatGPT for Prompt 1, and ZZZZZ for Prompt 2....

### Prompt 1
How do you create an XOR from only and/or/not gates?

### Response 1
To create an XOR (exclusive OR) gate using only AND, OR, and NOT gates, you can follow these steps. The XOR gate outputs true only when the inputs are different.

The truth table for XOR is:

| A | B | A XOR B |
|---|---|---------|
| 0 | 0 |    0    |
| 0 | 1 |    1    |
| 1 | 0 |    1    |
| 1 | 1 |    0    |

The Boolean expression for XOR can be derived as:\
A &oplus; B = (A &and; &not; B) &or; (&not; A &and; B)

This can be broken down into the following steps:

1. Create \(&not; A\) and \(&not; B\) using NOT gates.
1. Create \(A &and; &not; B\) and \(&not; A &and; B\) using AND gates.
1. Combine the results of the two AND gates using an OR gate.

Here is the step-by-step logic construction:

1. **NOT gates** to get \(&not; A\) and \(&not; B\):\
   NOT(A) &rarr; &not; A\
   NOT(B) &rarr; &not; B

1. **AND gates** to get \(A &and; &not; B\) and \(&not; A &and; B\):\
   A &and; &not; B &rarr; AND(A, &not; B)\
   &not; A &and; B &rarr; AND(&not; A, B)

1. **OR gate** to get the final result:\
   (A &and; &not; B) &or; (&not; A &and; B) &rarr; OR(AND(A, &not; B), AND(&not; A, B))

Putting it all together in a circuit diagram:

1. Input \(A\) goes to a NOT gate to produce \(&not; A\).
1. Input \(B\) goes to a NOT gate to produce \(&not; B\).
1. Input \(A\) and the output of the NOT gate for \(B\) go to an AND gate to produce \(A &and; &not; B\).
1. Input \(B\) and the output of the NOT gate for \(A\) go to an AND gate to produce \(&not; A &and; B\).
1. The outputs of the two AND gates go to an OR gate to produce the final output \(A &oplus; B\).

In terms of Boolean logic:\
XOR(A, B) = \(A &and; &not; B\) &or; \(&not; A &and; B\) 

This way, you have constructed an XOR gate using only AND, OR, and NOT gates.

### Changes 1
I needed XNOR, so changed it to:\
&not;\(\(A &and; &not; B\) &or; \(&not; A &and; B\)\)

### Prompt 2
My other prompt...

### Response 2
The other response...

### Changes 2
The other changes made...