"""
Copyright 2020, Masrik Dahir, All Right Reserved
"""
import string
from word2number import w2n
from nltk.corpus import wordnet
import time
import re
import nltk
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('omw-1.4')


def main():
    """
    the main function of hte root module
    """
    start = time.process_time()
    teacher = 'Security Implementing sport over'
    student = 'Implementation of protection play over'
    print(synonyms('sport'))
    print(justify(student, teacher))
    print(time.process_time() - start)


def justify(student: str, teacher: str) -> bool:
    """
    check if two string synonymous or not
    """
    if str(student).lower() == str(teacher).lower():
        return True
    else:
        return isSame(clean(str(teacher)), clean(str(student)))


def clean(phrase: str) -> list:
    """
    take the string and remove stop words, but do not remove 'not'
    make it lower
    lemmatize the word so, e,es,os,ing,etc.... gets removed
    remove special character
    break the string into a list of words by space and special character
    remove extra space
    then ut returns the list
    """
    root_word = []
    no_stop_word = []
    stopwords = nltk.corpus.stopwords.words('english')
    stopwords.remove('not')
    phrase = re.sub(' +', ' ', phrase.lower())
    tokens = re.split('\W+', phrase.rstrip())
    for j in tokens:
        if j not in stopwords:
            no_stop_word.append(j)
    while '' in no_stop_word:
        no_stop_word.remove('')

    return no_stop_word


def isSame(teacher: list, student: list) -> bool:
    """
    runs with all the synonyms for the list of words
    look for any synonyms of teacher list of words that is equal to the student
    the number of matchers is n
    if n is equal or greater than the length of teacher list and **special condition (intended to make the matching more leaner or stricter)** returns true
    """
    n = 0
    ps = nltk.PorterStemmer()
    if teacher == student:
        return True
    else:
        for i in student:
            for j in teacher:
                syn = synonyms(j)
                for k in syn:
                    if k[:1].lower() == i[:1].lower():
                        if ps.stem(i) == ps.stem(k):
                            n += 1
                            break
        if n >= len(teacher) and ((2*len(teacher) >= len(student)) and (2*len(student) >= len(teacher))):
            return True
        else:
            return False


def remove_punct(text: str) -> str:
    """
    remove the punctuation from a string
    """
    text_nopunct = "".join([char for char in text if char not in string.punctuation])
    return text_nopunct


def convert_number(text: str) -> int:
    """
    convert a string into a number if the string represent a written form of a number
    """
    return w2n.word_to_num(text)


def synonyms(text: str) -> list:
    """
    return the list of synonyms for a string
    """
    synonyms = []

    for syn in wordnet.synsets(text):
        for lm in syn.lemmas():
            synonyms.append(lm.name())

    no_duplicate = []
    for i in synonyms:
        if i not in no_duplicate:
            no_duplicate.append(i)
    if len(no_duplicate) == 0:
        no_duplicate.append(text)
    if text not in no_duplicate:
        no_duplicate.append(text)
    return no_duplicate

if __name__ == '__main__':
    main()
