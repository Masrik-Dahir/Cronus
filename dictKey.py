"""
Copyright 2020, Masrik Dahir, All Right Reserved
"""
import root
import xmlPursing
def delete_duplicate(a:dict) -> dict:
    """
    This function return a dictionary after deleting duplicate lists
    from its value
    """
    res = None
    if isinstance(a, dict):
        res = {}
        for i, j in a.items():
            if j not in res.values():
                res[i] = j
    if isinstance(a, list):
        res = []
        for i in a:
            if i not in res:
                res.append(i)
    return res

def get_value_any(a:dict, key:str) -> list or None:
    """
    get value from a key from a dictionary either from-id or to-id dictionary of ids
    """
    node = {}
    linking = {}
    if isinstance(a,str):
        node = xmlPursing.node(a)
        linking = xmlPursing.lf(a)
    if isinstance(a,list):
        node = xmlPursing.node_multiple(a)
        linking = xmlPursing.lf_multiple(a)
    for i,j in node.items():
        if i == key:
            return j
    for i, j in linking.items():
        if i == key:
            return j
    else:
        return None

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
    unmatched_index = []
    ind = None
    for i in instructor:
        for j in unmatched:
            if i == j:
                ind = instructor.index(i)
                unmatched_index.append(ind)
    return unmatched_index


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

def matched_value_advanced_key(instructor: list, student: list) -> list:
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
    ind = None
    matched_index = []
    for i in instructor:
        for j in matched:
            if i == j:
                ind = instructor.index(i)
                matched_index.append(ind)
    return matched_index

def get_key_any(a:dict, val:str)->str or None:
    """
    return the key that matches either from-id or to-id dictionary of ids
    they have separate keys
    """
    stat = None
    nodes = {}
    lf = {}
    if (isinstance(a,str)):
        nodes = xmlPursing.node(a)
        lf = xmlPursing.lf(a)
    if (isinstance(a, list)):
        nodes = xmlPursing.node_multiple(a)
        lf = xmlPursing.lf_multiple(a)
    if val in nodes.values():
        for key, value in nodes.items():
            if val == value:
                stat = key
    if val in lf.values():
        for key, value in lf.items():
            if val == value:
                stat = key
    return stat
def mismatched_key_list(instructor_directory: str or list, student_directory: str or list) -> list and float and float and float and int:
    """
    finds the unmatched key list from the instructor dictionary that were absent in student dictionary
    """
    list_i = []
    dict_key_i = {}
    dict_concept_i = {}
    dict_lf_i = {}
    list_s = []
    dict_key_s = {}
    dict_lf_s = {}
    dict_concept_s = {}
    dict_node_linking_i = {}
    dict_node_linking_s = {}
    rt = []

    if isinstance(instructor_directory, str):
        dict_key_i = xmlPursing.process_key(instructor_directory)
        dict_concept_i = xmlPursing.node(instructor_directory)
        dict_lf_i = xmlPursing.lf(instructor_directory)
        dict_node_linking_i.update(dict_concept_i)
        dict_node_linking_i.update(dict_lf_i)
    elif isinstance(instructor_directory, list):
        dict_key_i = xmlPursing.process_key_many(instructor_directory)
        dict_concept_i = xmlPursing.node_multiple(instructor_directory)
        dict_lf_i = xmlPursing.lf_multiple(instructor_directory)
        dict_node_linking_i.update(dict_concept_i)
        dict_node_linking_i.update(dict_lf_i)
    if isinstance(student_directory, str):
        dict_key_s = xmlPursing.process_key(student_directory)
        dict_concept_s = xmlPursing.node(student_directory)
        dict_lf_s = xmlPursing.lf(student_directory)
        dict_node_linking_s.update(dict_concept_s)
        dict_node_linking_s.update(dict_lf_s)
    elif isinstance(student_directory, list):
        dict_key_s = xmlPursing.process_key_many(student_directory)
        dict_concept_s = xmlPursing.node_multiple(student_directory)
        dict_lf_s = xmlPursing.lf_multiple(student_directory)
        dict_node_linking_s.update(dict_concept_s)
        dict_node_linking_s.update(dict_lf_s)
    num_i_node = len(dict_concept_i) + len(dict_concept_s) + len(dict_lf_i) + len(dict_lf_s)

    for key, value in dict_node_linking_i.items():
        if value not in list_i:
            list_i.append(value)
    for key, value in dict_node_linking_s.items():
        if value not in list_s:
            list_s.append(value)
    for value_i in list_i:
        for value_s in list_s:
            if (root.justify(value_i, value_s)):
                rt.append(value_i)
    num_node = 0
    num_lf = 0
    num_node_list = []
    num_lf_list = []

    for i in rt:
        if get_key_any(instructor_directory,i) in dict_concept_i:
            if get_key_any(instructor_directory,i) not in num_node_list:
                num_node_list.append(get_key_any(instructor_directory,i))
                num_node+=1
        if get_key_any(instructor_directory,i) in dict_lf_i:
            if get_key_any(instructor_directory, i) not in num_lf_list:
                num_lf_list.append(get_key_any(instructor_directory, i))
                num_lf+=1
    per_node = round((num_node/len(delete_duplicate(dict_concept_i)))*100,2)
    per_lf = round((num_lf / len(delete_duplicate(dict_lf_i)))*100,2)
    per_avg = round(((num_node+num_lf)/(len(delete_duplicate(dict_concept_i))+len(delete_duplicate(dict_lf_i))))*100,2)

    result = []
    for i in list_i:
        if i not in rt:
                if i not in result:
                    result.append(i)
    result_final = []
    for i in result:
        result_final.append(get_key_any(instructor_directory,i))
    return result_final, per_node, per_lf, per_avg, num_i_node

def word_per_concept(dir: str or list) -> float:
    """
    find average word per concept in student concept map
    """
    length_word = 0
    orphans = []
    dict = {}
    if (isinstance(dir, str)):
        dict = xmlPursing.node(dir)
        for key, value in xmlPursing.orphan_list(dir).items():
            orphans.append(value)
        for key, value in dict.items():
            if value not in orphans:
                for concept in value.split(' '):
                    length_word += len(concept.split(' '))
    if (isinstance(dir, list)):
        dict = xmlPursing.node_multiple(dir)
        for key, value in xmlPursing.orphan_list(dir).items():
            orphans.append(value)
        for key, value in dict.items():
            if value not in orphans:
                for concept in value.split(' '):
                    length_word += len(concept.split(' '))
    length_concept_dict = length_word/len(dict)
    return length_concept_dict


def main():
    a = r'ConceptMapFiles\CXLFiles\ComputerSecurity\Instructor\Module2UserAuthentication\Lesson3PasswordFilesFormats\Linux.cmap.cxl'
    b = 'CS_CIA_Triad.cmap.cxl'
    c = 'CS_Relationships.cmap.cxl'
    d = 'CS_Terms.cmap.cxl'
    e = 'ICSAnonymous1.cmap.cxl'
    x = r'ConceptMapFiles\CXLFiles\ComputerSecurity\Student\Module2UserAuthentication\UAAnonymous1.cmap.cxl'
    y = '.cmap.cxl'
    z = x + str(5) + y

    print(mismatched_key_list(a,x))


if __name__ == '__main__':
    main()