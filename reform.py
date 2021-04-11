"""
Copyright 2020, Masrik Dahir, All Right Reserved
"""
import compare
import root
import xmlParsing


def ndict(ins: dict, stu: dict) -> dict:
    """
    mark the dictionary keys that were absent in student dictionary for panda to color with CSS
    property
    """
    n_u_m = {}
    myString = ' #$#'
    missing = compare.get_cul(ins,stu)

    for i,j in missing.items():
        n_u_m[i] = [s + myString for s in j]

    for k_i, v_i in ins.items():
        for k_u, v_u in missing.items():
            if k_i == k_u:
                for u in v_i:
                    if u in v_u:
                        ind = v_i.index(u)
                        v_i[ind] = str(u) + myString
    return ins


def concept_dict (ins: dict) -> dict:
    """
    Create preposition without linking phrase dictionary
    """
    ins_c = {}
    for key, value in ins.items():
        dict_c_list = []
        for i in value:
            id = value.index(i)
            if id%2 == 0:
                dict_c_list.append(i)
        ins_c[key] = dict_c_list


    return ins_c

def comp(ins: dict, stu:dict) -> tuple and tuple:
    """
    Compare two concept_dict list of matched matched values of the dictionaries
    """
    ins_concept, extra_ins = concept(ins)
    stu_concept, extra_stu = concept(stu)
    res = []
    res_no_duplicates = []

    pes = []
    pes_no_duplicates = []
    for i in ins_concept:
        for j in stu_concept:
            if root.justify(str(i[0]), str(j[0])) and root.justify(str(i[1]), str(j[1])):
                res.append(i)
    for i in ins_concept:
        for j in extra_stu:
            if root.justify(str(i[0]), str(j[0])) and root.justify(str(i[1]), str(j[1])):
                pes.append(i)
    for i in res:
        if i not in res_no_duplicates:
            res_no_duplicates.append(i)
    for i in pes:
        if i not in pes_no_duplicates:
            pes_no_duplicates.append(i)

    return res_no_duplicates, pes_no_duplicates
def get_key_any(a:dict, val:list) -> list:
    """
    return the key that matches either from-id or to-id dictionary of ids
    they have separate keys
    """
    stat = None
    nodes = {}
    if (isinstance(a,str)):
        nodes = xmlParsing.node(a)
    if (isinstance(a, list)):
        nodes = xmlParsing.node_multiple(a)
    if val in nodes.values():
        for key, value in nodes.items():
            if val == value:
                stat = key
    return stat

def concept_score(instructor_directory: str or list,student_directory: str or list) -> dict and float:
    """
    :return the student concept dictionary, conception grade, and matched conception dictionary
    """
    ins = {}
    stu = {}
    ins_key = []

    if isinstance(instructor_directory, str):
        ins = xmlParsing.process(instructor_directory)
    elif isinstance(instructor_directory, list):
        ins = xmlParsing.process_multiple(instructor_directory)
    if isinstance(student_directory, str):
        stu = xmlParsing.process(student_directory)
    elif isinstance(student_directory, list):
        stu = xmlParsing.process_multiple(student_directory)

    ins_comcept, extra_ins = concept(ins)
    stu_concept, extra_stu = concept(stu)
    match, extra_match = comp(ins, stu)

    conception_score = round((len(match)+len(extra_match))/len(ins_comcept)*100,2)
    if conception_score < 0:
        conception_score = 0
    if conception_score > 100:
        conception_score = 100
    for i in extra_match:
        match.append(i)
    for i in match:
        ins_key.append([get_key_any(instructor_directory, i[0]),get_key_any(instructor_directory,i[1])])
    result = []
    for i in ins_key:
        if i not in result:
            result.append(i)

    result_single_list = []
    for i in result:
        for m in i:
            if m not in result_single_list:
                result_single_list.append(m)

    return stu_concept, conception_score, result_single_list
def concept(ins: dict):
    ins_c = {}
    con = {}
    extra_con = {}
    con_values = []
    con_values_extra = []
    n = 1
    m = 1

    for key, value in ins.items():
        dict_c_list = []
        for i in value:
            id = value.index(i)
            if id%2 == 0:
                dict_c_list.append(i)
        ins_c[key] = dict_c_list


    for key, value in ins_c.items():
        for i in value:
            lenth = len(value)
            id = value.index(i)
            if id+1 < lenth:
                con[m] = [value[id], value[id + 1]]
                m += 1
                for num in range(id + 1, lenth):
                    if num < lenth:
                        extra_con[n] = [value[id], value[num]]
                        n += 1

    for key, value in con.items():
        if value not in con_values:
            con_values.append(value)

    for key, value in extra_con.items():
        if value not in con_values_extra:
            if value not in con_values:
                con_values_extra.append(value)
    return con_values, con_values_extra


def main():
    a = 'CS_Overview.cmap.cxl'
    b = 'CS_CIA_Triad.cmap.cxl'
    c = 'CS_Relationships.cmap.cxl'
    d = 'CS_Terms.cmap.cxl'
    e = 'ICSAnonymous1.cmap.cxl'
    x = 'ConceptMapFiles\CXLFiles\ComputerSecurity\Student\Module1IntroductionComputerSecurity\ICSAnonymous'
    y = '.cmap.cxl'

    ins = r'ConceptMapFiles\CXLFiles\ComputerSecurity\Instructor\Module1IntroductionComputerSecurity\Lesson1ComputerSecurityOverview\CS_Overview.cmap.cxl'
    stu = r'ConceptMapFiles\CXLFiles\ComputerSecurity\Student\Module1IntroductionComputerSecurity\ICSAnonymous6.cmap.cxl'
    print(concept_score(ins, stu))


if __name__ == '__main__':
    main()
