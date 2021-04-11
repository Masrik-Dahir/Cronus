"""
Copyright 2020, Masrik Dahir, All Right Reserved
"""
import time
import xmlParsing
import root

total_match = []
grade_list = []
c_u_l = {}
partial = {}
cmap = {}


def get_cmap(ins: dict, stu: dict) -> dict:
    """
    This function return the unique comparison key for instructor and student dictionary
    """
    engine(ins, stu)
    return cmap

def get_summery_text(ins: dict, stu: dict) -> str:
    """
    This function return summery text: matched branch, mismatched branch, partially
    matched branch, extra branch
    """
    ins_c = dict(ins)
    cm = get_cmap(ins, stu)
    return summery_text(cm, grade_list, ins_c)

def get_cul(ins: dict, stu: dict) -> dict:
    """
    This function return the unmatched concepts and linking phrases from instructor
    dictionary in a dictionary format
    """
    get_cmap(ins,stu)
    return c_u_l
def getM_p_u(ins: dict, stu:dict) -> list:
    """
    This function return the matched, partially matched, mismatched, and extra
    branched in a list
    """
    summery, comparison, cmap_dict, grade, m_p_u, info = engine(ins, stu)
    return m_p_u
def main():
    """
    The main function that print out the entire function
    """
    start = time.process_time()
    a = 'CS_Overview.cmap.cxl'
    b = 'CS_CIA_Triad.cmap.cxl'
    c = 'CS_Relationships.cmap.cxl'
    d = 'CS_Terms.cmap.cxl'
    e = 'ICSAnonymous1.cmap.cxl'
    x = 'ConceptMapFiles\CXLFiles\ComputerSecurity\Student\Module1IntroductionComputerSecurity\ICSAnonymous'
    y = '.cmap.cxl'
    z = x + str(5) + y

    ins = xmlParsing.combine(a)
    stu = xmlParsing.combine(z)
    total_match.clear()

    summery, comparison, cmap_dict, grade, m_p_u, info = engine(ins, stu)


    print(summery)
    print(comparison)
    print(cmap_dict)
    print(grade)
    print(m_p_u)
    print(info)

    print('**************************************************')
    print('The program took ' + str(time.process_time() - start) + ' seconds')
    print('**************************************************')


def engine(ins: dict, stu: dict):
    """
    the function reset the value of global variables which is necessary for other function to run
    generate cmap_key
    generate partial
    generate grade_list
    generate total match
    main function should call or print out this function before calling any other functions
    printing the function would provide all the detailed value of comparison
    """
    partial.clear()
    grade_list.clear()
    total_match.clear()
    ins_copy = {}
    stu_copy = {}

    ins_copy = dict(ins)
    stu_copy = dict(stu)

    st = "Fully or Partially Matched: \n"
    for a, b in ins.items():
        branch_i = b
        key_s = find_match(stu, branch_i)
        key_i = a
        score = 0
        unmatched = []
        if key_s != 0:
            ins = {k: v for k, v in ins.items() if v != branch_i}
            branch_s = get_list_from_key(stu, key_s)
            partial[int(str(key_i).replace('{', '').replace('}', ''))] = int(str(key_s))
            if len(partial) != 0:
                for key_p, value_p in partial.items():
                    lis = []
                    sum = 0
                    number = 0
                    total = 0
                    li = ins_copy.get(key_p)
                    unmatched = unmatched_value_advanced(ins_copy.get(key_p), stu_copy.get(value_p))
                    for i in unmatched:
                        lis.append(li.index(i))
                    total = (len(ins_copy.get(key_p)) * (len(ins_copy.get(key_p)) + 1)) / 2
                    for i in lis:
                        number = len(ins_copy.get(key_p)) - i
                        sum += number
                    score = (total - sum) / total
            grade_list.append(score)
            st += 'Instructor: ' + str(branch_i) + '\nStudent: ' + str(
                get_list_from_key(stu, str(key_s))) + '\nUnmatched: ' + str(unmatched) + '\n' + 'Score = ' + str(
                score) + '\n\n'
            c_u_l[a] = unmatched

            total_match.append(len(branch_i) - len(unmatched))
            stu = {k: v for k, v in stu.items() if k != key_s}
    st += 'Student Missed: \n'
    for key, value in ins.items():
        st += str(value) + '\n'
        score = 0
        grade_list.append(score)
        st += 'Score = ' + str(score) + '\n\n'
        c_u_l[key] = value
    st += '\n\nStudent Wrote Extra: \n'
    for key, value in stu.items():
        st += str(value) + '\n'
    st += '\n\n'

    cmap = cmap_key(partial, ins, stu)
    summ = summery_text(cmap, grade_list, ins_copy)
    gr = round(grade(grade_list), 2)
    m_p_u = summery(cmap,grade_list)
    m = m_p_u[0]
    p = m_p_u[1]
    u = m_p_u[2]
    e = m_p_u[3]
    info = 'Matched Branch:\t\t\t' + str(m) + '\lPartially Matched Branch:\t' + str(
        p) + '\lMismatched Branch:\t\t' + str(u) + '\lExtra Branch:\t\t\t\t' + str(e)


    return summ, st, cmap, gr, m_p_u, info


def summery(cmap_key: dict, grade_list: list):
    """
    creates the list of score
    matched = m = ser[0] = the first element of the list
    partial = p = ser[1] = the second element of the list
    matched = u = ser[2] = the third element of the list
    matched = e = ser[3] = the fourth element of the list
    """
    m = 0
    p = 0
    u = 0
    e = 0
    for i in grade_list:
        if i == 1:
            m += 1
    for key, value in cmap_key.items():
        if str(key).isdigit() and str(value).isdigit():
            p += 1
        elif not str(key).isdigit():
            if "None " in key:
                e += 1
        elif value is None:
            u += 1
    p = p - m
    ser = [m, p, u, e]
    return ser


def summery_text(cmap_key: dict, grade_list: list, ins_copy: dict) -> str:
    """
    turn the list of summery into a str return statement
    """
    s = summery(cmap_key, grade_list)
    sum = 0
    for i in grade_list:
        sum += i
    g = (sum / len(grade_list)) * 100

    p_sum = 0
    for i in total_match:
        p_sum += i
    items = 0
    for a, b in ins_copy.items():
        items += len(b)
    match_percent = (p_sum / items) * 100

    all_summery = "\nSummery\nFully Matched: " + str(s[0]) + '\nPartially Matched: ' + str(s[1]) + '\nMissed: ' + str(
        s[2]) + '\nExtra: ' + str(s[3]) + '\nMatch Percent: ' + str(match_percent) + '\nGrade: ' + str(g) + '\n'
    return all_summery


def cmap_key(partial: dict, ins: dict, stu: dict) -> dict:
    """
    creates the cmap_key
    cmap_key is a distinct dictionary of matched keys from instructor and student dictionary
    """
    cmap.clear()
    cmap.update(partial)
    if len(ins) != 0:
        for i, j in ins.items():
            cmap[i] = None
            # grade_list.append(0)
    if len(stu) != 0:
        for i, j in stu.items():
            cmap["None " + str(i)] = i
    return cmap


def grade(grade_list: list) -> float:
    """
    return overall grade in percent from the grade_list
    """
    sum = 0
    for i in grade_list:
        sum += i
    # print(len(grade_list))
    return (sum / len(grade_list)) * 100


def find_match(dictionary_i: dict, lis: list) -> int:
    """
    Most important function of the module
    It compares the branches of dictionaries (branch of a instructor dictionary to the student dictionary)
    and return the matching key of the student dictionary
    """
    high = 0
    h_key = 0
    h_point = 0
    m_l = []
    i_l_l = []
    for key, value in dictionary_i.items():
        point = 0
        val = 0
        i_l_l = value
        s_l_l = lis
        m_l = matched_value_advanced(i_l_l, s_l_l)
        for i, e in enumerate(m_l):
            point += (len(i_l_l) - i_l_l.index(e))
            if point > h_point:
                h_point = point
        q = 0
        for i in range(len(i_l_l) - 1, -1, -1):
            if len(i_l_l) == len(lis):
                if root.justify(i_l_l[i], lis[i]):
                    q += 1
                    if q == len(i_l_l):
                        h_key = key
                    else:
                        val = len(m_l)
                        if val > high and h_point > point:
                            high = val
                            h_key = key
        val = len(m_l)
        if val > high and h_point > point:
            high = val
            h_key = key
        elif val > high:
            high = val
            h_key = key
    return h_key


def unmatched_value(instructor: list, student: list) -> list:
    """
    return the unmatched value set in a list from two list
    Natural Language Processing is not applied
    mainly intended for general comparison purposes
    for advanced comparison use the advanced_unmatched_value()
    """
    matched = []
    matched = set(student).intersection(set(instructor))
    unmatched = set(instructor) - matched
    return list(unmatched)


def unmatched_value_advanced(instructor: list, student: list) -> list:
    """
    find the unmatched values from student and teacher list and append it to a list which is returned
    Natural Language Processing is Applied
    remove the block word from each element of the list and run all the synonyms to justify the match
    more leaner/stricter matching can be implemented by changing interaction between n, teacher, and student on root.isSame()
    """
    matched = []
    for i in set(student):
        for j in set(instructor):
            if root.justify(j, i):
                matched.append(j)
    unmatched_ins = set(instructor) - set(matched)
    unmatched_stu = set(student) - set(matched)

    u_m_i_c = unmatched_ins.copy()
    u_m_i_c.update(unmatched_stu)
    unmatched = list(u_m_i_c)
    return list(unmatched_ins)


def matched_value_advanced(instructor: list, student: list) -> list:
    """
    find the matched values from student and teacher list and append it to a list which is returned
    Natural Language Processing is Applied
    remove the block word from each element of the list and run all the synonyms to justify the match
    more leaner matching can be implemented by changing interaction between n, teacher, and student on root.isSame()
    """
    matched = []
    for i in set(student):
        for j in set(instructor):
            if root.justify(i, j):
                matched.append(j)
    return matched


def matched_value(instructor: list, student: list) -> list:
    """
    find the matched values from student and teacher list and append it to a list which is returned
    Natural Language processing is not applied
    mainly intended for general comparison purposes
    for advanced comparison use the advanced_matched_value()
    """
    matched = []
    matched = list(set(student).intersection(set(instructor)))
    return matched


def unmatched_key(instructor: list, student: list) -> list:
    """
    return the index+1 of a instructor list for any unmatched value and append it to a list
    """
    matched = []
    ind = []
    c = (set(student) - set(instructor))
    d = (set(instructor) - set(student))
    c.update(d)

    for i in set(student):
        for j in set(instructor):
            if root.justify(j, i):
                matched.append(j)
    unmatched_ins = set(instructor) - set(matched)
    unmatched_stu = set(student) - set(matched)
    for i in set(unmatched_ins):
        for index, s in enumerate(instructor):
            if root.justify(i, s):
                ind.append(index + 1)
    return ind


def unmatched_dictionary(instructor: list, student: list) -> dict:
    """
    return a dictionary of unmatched key and value previously found on unmatched_key, and unmatched_value_advanced
    """
    dict = []
    key = unmatched_key(instructor, student)
    values = unmatched_value_advanced(instructor, student)
    dict = {k: v for k, v in zip(key, values)}

    return dict


def get_lenth(list: list) -> int:
    """
    return the length of a list
    """
    e = 0
    for i in list:
        e += 1
    return e


def get_key(dictionary: dict, val: list) -> int:
    """
    return the key of a list if the list if the value matched with any value of the dictionary
    """
    stat = -1
    for key, value in dictionary.items():
        if val == value:
            stat = key
            break
    return stat


def get_list_from_key(dictionary: dict, k: str) -> list:
    """
    return the list of a list if the key if the key matched with any key of the dictionary
    """
    v = []
    for key, value in dictionary.items():
        if root.justify(key, k):
            v = value
    return v


def intersection(Instructor: list, Student: list) -> list:
    """
    find intersection of two lists
    intersection means the common values
    """
    return list(set(i for i in Instructor).intersection(set(i for i in Student)))


def union(Instructor: list, Student: list) -> list:
    """
    find union of the wo lists
    union means all the values of combining instructor and student excluding doubles
    """
    return list(set(i for i in Instructor).union(set(i for i in Student)))


def h_length_branch(dictionary: dict) -> list:
    """
    find the highest lengh list from a dictionary
    """
    value = 0
    h_value = 0
    h_total = 0
    h_value_list = []
    for key, values in dictionary.items():
        value = len(values)
        if value > h_value:
            h_value = value
            h_value_list = values
            a = [len(i) for i in values]
            total = 0
            for ele in range(0, len(a)):
                total = total + a[ele]
            h_total = total
            h_value = value
            h_value_list = values
        if h_value == value:
            a = [len(i) for i in values]
            total = 0
            for ele in range(0, len(a)):
                total = total + a[ele]
            if total > h_value:
                h_total = total
                # h_value = value
                h_value_list = values
            h_e = 0
            if total == h_total:
                num_words = [len(sentence.split('e')) for sentence in values]
                e = 0
                for ele in range(0, len(num_words)):
                    e = e + num_words[ele]
                if e > h_e:
                    h_e = e
                    # h_total = total
                    # h_value = value
                    h_value_list = values
    return h_value_list


def get_index(lis: list, val: str) -> int:
    """
    return the index of value on a list
    """
    index = None
    for i, e in enumerate(lis):
        if root.justify(e, val):
            index = i
    return index


def check_index_list(any_list: list, index: int) -> bool:
    """
    check whether the index exist on the list or not
    """
    return (index < len(any_list))


if __name__ == "__main__":
    main()
