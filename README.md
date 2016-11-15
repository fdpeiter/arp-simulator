Simple Net Simulator
======================

This package is an implementation of an final assigment for the course of Computer Networks I.
It consists in simulating an virtual network from an formatted input file.
After parsing the input, you can execute ping commands between nodes.

SETUP
=====

 1. Simple execute the setup.py for automatic install dependencies
      python setup.py

USAGE
=====
 
 1. Check the input format example and documentation in the docs/input_format.txt
 
 2. Proceed to create an .txt with the nodes, routers and routertables of the scenario you want to simulate.
 
 3. Execute the program, pass the input file that you created an inform the order of communication between the nodes.
 
        python input.txt n1 n2 n3
 
    In this example, the n1 will proceed to perform an ECHO REQUEST to n2, then, n2 will perform an ECHO REQUEST to n3.
    
 4. The result will be printed in the console.

ABOUT THE CODE
==============



CONTACT
=======

Please send bug reports, patches, and other feedback to

  fdpeiter@gmail.com
