# Cronus: An Automated Feedback Tool for Concept Maps Comparing
Security And Forensics Engineering Lab, Virginia Commonwealth University

Faculty Professor: Dr. Irfan Ahmed

The repository is a research project which I have been conducting under the SAFE Lab of VCU. The project intends to compare camp files and provide similarities. It is written in python- the program also involves natural language processing and machine learning.

Steps

First .cmap files need to be extracted as a .cxl file
The xmlPursing.py convers .cxl file into a sorted dictionary
compare.py use xmlPursing to compare the simmilarities and print out a. matched, b. partial match, c. unmatched, d. extra, e. pairs that matched/partially matched for instructor and student, f. cmap key, an unique dictionary that encode all the information,
Natural Language Processing is applied to compare strings
root.py excluse stop words, remove special character, and run down synonyms to match with the instructor string
