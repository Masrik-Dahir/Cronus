"""
Copyright 2020, Masrik Dahir, All Right Reserved
"""
a_string = None
dictConcepts = {}
number_of_lines = 0
number_of_words = 0
number_of_characters = 0
branchLen = 0
name = None


def numLine(name):
    try:
        file = open(name, "r")
        number_of_lines = 0
        number_of_words = 0
        number_of_characters = 0
        for line in file:
            line = line.strip("\n")  # won't count \n as character
            words = line.split()
            number_of_lines += 1
            number_of_words += len(words)
            number_of_characters += len(line)
        file.close()
        return number_of_lines
    except FileNotFoundError:
        print("The file do not exist. Please check your file directory again.")


def anyLine(name, n):
    try:
        with open(name) as f:
            lines = f.readlines()
            desired_line = lines[n]
            return desired_line
    except FileNotFoundError:
        print("The file do not exist. Please check your file directory again.")


def remove_space(string):
    return string.strip()


def split(name):
    for i in range(0, numLine(name)):
        a_string = anyLine(name, i).split('\t')
        if len(a_string) == 1:
            print("Topic: " + a_string[0])
        elif len(a_string) == 3:
            dictConcepts[a_string[0], a_string[2].rstrip('\n')] = a_string[1]
        else:
            print("different type of concept")


def main(name):
    name = input("Enter the directory (of propositions of texts of a .cmap file)\n")
    print('\n')
    if name.endswith('.txt'):
        split(name)
    else:
        print("This is not a txt file. Please enter a valid directory of a text file. ")
    try:
        for key in dictConcepts:
            print(key, ':', dictConcepts[key])
    except KeyError:
        print('There is no concept-relation to show!')


main(name)
