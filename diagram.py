"""
Copyright 2020, Masrik Dahir, All Right Reserved
"""
import time

from graphviz import Digraph
import xmlParsing
import dictKey
import reform
import compare
import os
import xlsxwriter
from os import listdir
from os.path import isfile, join
import sys
os.environ["PATH"] += os.pathsep + r'C:\Program Files\Graphviz\bin'


def grading_system(grade: float):
    if (grade >= 90):
        return 'A'
    elif (grade >= 80):
        return 'B'
    elif (grade >= 70):
        return 'C'
    elif (grade >= 60):
        return 'D'
    elif (grade < 60):
        return 'F'
    else:
        return None

def simplyfy(text:str) -> str:
    """
    This function remove tab, line and other string formating away and return the string
    in a special format that represent that fit nicely into the box of the nodes in dia()
    """
    text = text.replace('\r', '')
    if len(text) < 10 or len(text.split(' ')) < 2:
        return text
    else:
        sum = 0
        lineLength = 0
        l = text.split(' ')
        for x in l:
            sum = sum + len(x) + 1
            if sum >= 10:
                lineLength = sum
                return text[:lineLength] + '\n' + simplyfy(text[lineLength:])
        return text[:lineLength] + '\n' + simplyfy(text[lineLength:])


def del_duplicate(lis: list) -> list:
    """
    Delete the duplicate element from a list
    """
    res = []
    for i in lis:
        if i not in res:
            res.append(i)

    return res


def name(stu: str or list) -> str:
    """
    retunrs the last name of a file from its directory
    """
    li = []
    nm = None
    if isinstance(stu, str):
        li = stu.split('\\')
    if isinstance(stu, list):
        li = stu[len(stu) - 1].split('\\')
    nm = li[len(li) - 1].replace('.cxl', '').replace('.cmap', '')
    return nm


def get_value_any(a: str or list, key: str) -> list or None:
    """
    get value from a key from a dictionary either from-id or to-id dictionary of ids
    """
    node = {}
    linking = {}
    if isinstance(a, str):
        node = xmlParsing.node(a)
        linking = xmlParsing.lf(a)
    if isinstance(a, list):
        node = xmlParsing.node_multiple(a)
        linking = xmlParsing.lf_multiple(a)
    for i, j in node.items():
        if i == key:
            return j
    for i, j in linking.items():
        if i == key:
            return j
    else:
        return None


def n_or_l(a:dict, key:str) -> 1 or 2 or None:
    """
    :return 1 if the value represented by the key is a node
    :return 2 if the value represented by the key is a linking phrase
    """
    node = {}
    linking = {}
    if isinstance(a, str):
        node = xmlParsing.node(a)
        linking = xmlParsing.lf(a)
    if isinstance(a, list):
        node = xmlParsing.node_multiple(a)
        linking = xmlParsing.lf_multiple(a)
    for i, j in node.items():
        if i == key:
            return 1
    for i, j in linking.items():
        if i == key:
            return 2
    else:
        return None


def dia(a:str or list, e: str or list, con = 1/3, mis = 1/3, hie = 1/3, curve = 0, isView = True):
    """
    :returns matched branch, missed branch, extra branch, partially matched branch, total match (%),
    Concept Match (%), hierarchy match (%) and grade
    create 2 diagram PDF
    """
    fr_s = '30'
    id_dict = None
    id_dict_student = None
    ins = {}
    stu = {}
    unmatched = None
    grade = None
    info = None
    leaf_num = 1
    per_node, per_lf, per_avg = 0, 0, 0
    A = None
    B = None
    C = None
    D = None
    E = None
    F = None
    G = None
    H = None
    I = None
    J = None
    K = None
    M = None
    L = None
    P = None
    Q = None

    start = time.process_time()
    sub_map_instructor = []
    stu_concept, concept_score, conception_match = reform.concept_score(a, e)
    concept_score = 100 - concept_score
    if isinstance(a, str) and isinstance(e, str):
        id_dict = xmlParsing.id_dict(a)
        id_dict_student = xmlParsing.id_dict(e)
        leaf_num = xmlParsing.num_orphan(e)
        ins = xmlParsing.process(a)
        stu = xmlParsing.process(e)
        unmatched, per_node, per_lf, per_avg, all_node = dictKey.mismatched_key_list(a, e)
        L = int(all_node)
        for key, value in xmlParsing.process(a).items():
            if value[0] not in sub_map_instructor:
                sub_map_instructor.append(value[0])
    if isinstance(a, list) and isinstance(e, str):
        id_dict = xmlParsing.id_dict_multiple(a)
        id_dict_student = xmlParsing.id_dict(e)
        leaf_num = xmlParsing.num_orphan(e)
        ins = xmlParsing.process_multiple(a)
        stu = xmlParsing.process(e)
        unmatched, per_node, per_lf, per_avg, all_node= dictKey.mismatched_key_list(a, e)
        L = int(all_node)
        for key, value in xmlParsing.process_multiple(a).items():
            if value[0] not in sub_map_instructor:
                sub_map_instructor.append(value[0])
    if isinstance(a, list) and isinstance(e, list):
        id_dict = xmlParsing.id_dict_multiple(a)
        id_dict_student = xmlParsing.id_dict_multiple(e)
        leaf_num = xmlParsing.num_orphan(e)
        ins = xmlParsing.process_multiple(a)
        stu = xmlParsing.process_multiple(e)
        unmatched, per_node, per_lf, per_avg, all_node = dictKey.mismatched_key_list(a, e)
        L = int(all_node)
        for key, value in xmlParsing.process_multiple(a).items():
            if value[0] not in sub_map_instructor:
                sub_map_instructor.append(value[0])
    if isinstance(a, str) and isinstance(e, list):
        id_dict = xmlParsing.id_dict(a)
        id_dict_student = xmlParsing.id_dict_multiple(e)
        leaf_num = xmlParsing.num_orphan(e)
        ins = xmlParsing.process(a)
        stu = xmlParsing.process_multiple(e)
        unmatched, per_node, per_lf, per_avg, all_node = dictKey.mismatched_key_list(a, e)
        L = int(all_node)
        for key, value in xmlParsing.process(a).items():
            if value[0] not in sub_map_instructor:
                sub_map_instructor.append(value[0])

    summery, comparison, cmap_dict, grade, m_p_u, info = compare.engine(ins, stu)
    B = int(m_p_u[0])
    C = int(m_p_u[1])
    D = int(m_p_u[2])
    E = int(m_p_u[3])

    dot = Digraph(comment='The Round Table')
    pot = Digraph(comment='The Round Table')
    if id_dict is not None and unmatched is not None and id_dict_student is not None:
        n = []
        n_m = []
        t = []
        t_m = []
        for key, value in xmlParsing.orphan_list(a).items():
            dot.node(key, value, style='filled',shape='rect', Gsplines='true', fontsize = fr_s)
        for key, value in id_dict.items():
            if n_or_l(a, value[0]) == 1:
                if value[0] in unmatched:
                    n.append(value[0])
                    t.append(value[0])
                    # Node unmatched
                    if get_value_any(a, value[0]) in sub_map_instructor:
                        dot.node(value[0], simplyfy(get_value_any(a, value[0])), style='filled', fillcolor='#FFB6C1',
                                 shape='doubleoctagon', Gsplines='true', fontsize = fr_s)
                    else:
                        dot.node(value[0], simplyfy(get_value_any(a, value[0])), style='filled', fillcolor='#FFB6C1',
                                 shape='rect', Gsplines='true', fontsize = fr_s)
                else:
                    n.append(value[0])
                    n_m.append(value[0])
                    t.append(value[0])
                    t_m.append(value[0])
                    # Node matched
                    if get_value_any(a, value[0]) in sub_map_instructor:
                        dot.node(value[0], simplyfy(get_value_any(a, value[0])), style='filled', fillcolor='white',
                                 shape='doubleoctagon', Gsplines='true', fontsize = fr_s)
                    else:
                        dot.node(value[0], simplyfy(get_value_any(a, value[0])), style='filled', fillcolor='white',
                                 shape='rect', Gsplines='true', fontsize = fr_s)
                if value[1] in unmatched:
                    t.append(value[1])
                    # linking phrase unmatched
                    dot.node(value[1], simplyfy(get_value_any(a, value[1])), shape='none', fontcolor='red',
                             Gsplines='true', fontsize = fr_s)
                else:
                    t.append(value[1])
                    t_m.append(value[1])
                    # linking phrase matched
                    dot.node(value[1], simplyfy(get_value_any(a, value[1])), shape='none', fontcolor='black',
                             Gsplines='true', fontsize = fr_s)
                dot.edge(value[0], value[1], constraint='true')
                # for i in conception_match:
                #     if (i[0] is simplyfy(get_value_any(a, value[0]))) and (i[1] is simplyfy(get_value_any(a, value[1]))):
                #         dot.edge(value[0], value[1], constraint='true', arrowhead='open', fontsize=fr_s)
                #     else:
                #         dot.edge(value[0], value[1], constraint='true', arrowhead='open', style='dashed', fontsize=fr_s)

            if n_or_l(a, value[0]) == 2:
                # linking phrase unmatched
                if value[0] in unmatched:
                    t.append(value[0])
                    dot.node(value[0], simplyfy(get_value_any(a, value[0])), shape='none', fontcolor='red',
                             Gsplines='true', fontsize = fr_s)
                # linking phrase matched
                else:
                    t.append(value[0])
                    t_m.append(value[0])
                    dot.node(value[0], simplyfy(get_value_any(a, value[0])), shape='none', fontcolor='black',
                             Gsplines='true', fontsize = fr_s)
                # Node unmatched
                if value[1] in unmatched:
                    t.append(value[1])
                    n.append(value[1])
                    if get_value_any(a, value[1]) in sub_map_instructor:
                        dot.node(value[1], simplyfy(get_value_any(a, value[1])), style='filled', fillcolor='#FFB6C1',
                                 shape='doubleoctagon', Gsplines='true', fontsize = fr_s)
                    else:
                        dot.node(value[1], simplyfy(get_value_any(a, value[1])), style='filled', fillcolor='#FFB6C1',
                                 shape='rect', Gsplines='true', fontsize = fr_s)
                # Node matched
                else:
                    t.append(value[1])
                    t_m.append(value[1])
                    n.append(value[1])
                    n_m.append(value[1])
                    if get_value_any(a, value[1]) in sub_map_instructor:
                        dot.node(value[1], simplyfy(get_value_any(a, value[1])), style='filled', fillcolor='white',
                                 shape='doubleoctagon', Gsplines='true', fontsize = fr_s)
                    else:
                        dot.node(value[1], simplyfy(get_value_any(a, value[1])), style='filled', fillcolor='white',
                                 shape='rect', Gsplines='true', fontsize = fr_s)
                # dot.edge(value[0], value[1], constraint='true')
                if (value[1] in conception_match):
                    dot.edge(value[0], value[1], constraint='true', arrowhead='open', fontsize=fr_s)
                else:
                    dot.edge(value[0], value[1], constraint='true', arrowhead='open', style='dashed', fontsize=fr_s)


        n = del_duplicate(n)
        n_m = del_duplicate(n_m)
        t = del_duplicate(t)
        t_m = del_duplicate(t_m)

        dot.node("Stat", 'SUMMERY\n\n' + info + "\lTotal Match:\t\t" + str(
            per_avg) + " %\lConcept Match:\t" + str(
            per_node) + " %\lLink. Phr. Match:\t"+str(per_lf) +
                 ' %\lMisconception:\t' + str(concept_score) + ' %\lHierarchy Match:\t'+str(grade)+" %\l", style='filled',
                 fillcolor='#F5FFFA', shape='component',
                 Gsplines='true', fontsize = fr_s)
        grade_result = float(round(per_node*con + (100 - concept_score)*mis + grade*hie,2))
        dot.node("Grade", 'Grade:\t' + str(grade_result) + '%\t' + grading_system(grade_result + curve),
                 style='filled', fillcolor='#FFEBCD', shape='note',
                 Gsplines='true', fontsize = fr_s)
        F = float(per_avg)
        G = float(per_node)
        H = float(per_lf)
        I = float(concept_score)
        J = float(grade)
        K = float(round(per_node*con + (100 - concept_score)*mis + grade*hie,2))

        dot.edge('Stat', 'Grade', constraint='true', arrowhead='inv', color = "black", fontsize = fr_s)

        # for i in conception_match:
        #     if (i[0] is not None) and (i[1] is not None):
        #         dot.edge(i[0],i[1], constraint='true', arrowhead='open', style= 'dashed', color = "#0316D1",fontsize = fr_s)

        nm_instructor = name(a)
        nm_student = name(e)
        A = str(nm_student)

        bran = {}
        branch_num = 0
        node_num = 0
        linking_num = 0
        preposition_num = 0
        orphan_num = 0
        sub_map_num = 0
        student_node = []
        student_linking = []
        student_orphan = []
        sub_map = []
        pot.node('Student', 'Student: ' + str(nm_student), style='filled', fillcolor='gold', shape='component', fontsize = fr_s)

        if (isinstance(e, str)):
            for key, value in xmlParsing.process(e).items():
                if value[0] not in sub_map:
                    sub_map.append(value[0])
        if (isinstance(e, list)):
            for key, value in xmlParsing.process_multiple(e).items():
                if value[0] not in sub_map:
                    sub_map.append(value[0])
        for key, value in id_dict_student.items():
            if n_or_l(e, value[0]) == 1:
                if value[0] not in student_node:
                    student_node.append(value[0])
                if value[1] not in student_linking:
                    student_linking.append(value[1])
                if get_value_any(e, value[0]) in sub_map:
                    pot.node(value[0], simplyfy(get_value_any(e, value[0])), style='filled', fillcolor='white',
                             shape='doubleoctagon', fontsize = fr_s)
                else:
                    pot.node(value[0], simplyfy(get_value_any(e, value[0])), style='filled', fillcolor='white',
                             shape='rect', fontsize = fr_s)
                pot.node(value[1], simplyfy(get_value_any(e, value[1])), shape='none', fontsize = fr_s)
            if n_or_l(e, value[0]) == 2:
                if value[1] not in student_node:
                    student_node.append(value[1])
                if value[0] not in student_linking:
                    student_linking.append(value[0])
                pot.node(value[0], simplyfy(get_value_any(e, value[0])), shape='none', fontsize = fr_s)
                if get_value_any(e, value[1]) in sub_map:
                    pot.node(value[1], simplyfy(get_value_any(e, value[1])), style='filled', fillcolor='white',
                             shape='doubleoctagon', fontsize = fr_s)
                else:
                    pot.node(value[1], simplyfy(get_value_any(e, value[1])), style='filled', fillcolor='white',
                             shape='rect', fontsize = fr_s)
            pot.edge(value[0], value[1], constraint='true', fontsize = fr_s)

        if (isinstance(e, str)):
            bran = xmlParsing.process(e)
            for nod in xmlParsing.node(e):
                if nod not in student_node:
                    student_orphan.append(nod)
            for l in xmlParsing.lf(e):
                if l not in student_linking:
                    student_linking.append(l)
        if (isinstance(e, list)):
            bran = xmlParsing.process_multiple(e)
            for nod in xmlParsing.node_multiple(e):
                if nod not in student_node:
                    student_orphan.append(nod)
            for l in xmlParsing.lf_multiple(e):
                if l not in student_linking:
                    student_linking.append(l)
        for value in student_orphan:
            pot.node(value, simplyfy(get_value_any(e, value)), style='filled', fillcolor='white', shape='rect', fontsize = fr_s)

        branch_num = len(bran)
        node_num = len(student_node)
        linking_num = len(student_linking)
        orphan_num = len(student_orphan)
        preposition_num = len(stu_concept)
        sub_map_num = len(sub_map)

        pot.node("statictics", "STATISTICS\n\lBranch:\t\t" + str(branch_num)+'\lNode:\t\t'+str(node_num)+'\lLinking Phrase:\t'+
                 str(linking_num)+"\lOrphan:\t\t"+str(orphan_num)+"\lLeaf Node:\t"+str(leaf_num)+"\lPreposition:\t"+str(preposition_num) + "\lSub Map:\t\t"+
                 str(sub_map_num)+'\lAvg Word Per Concept:\t'+str(round(dictKey.word_per_concept(e),2))+'\l', style='filled',fillcolor='#F5FFFA', shape='component',Gsplines='true', fontsize = fr_s)
        title = ''
        created =''
        modified =''
        language = ''
        format = ''
        publisher = ''
        width = 0
        height = 0
        for key, value in xmlParsing.information(e).items():
            if str(key) == "title":
                title = str(value)
            if str(key) == 'created':
                created = str(value)
            if str(key) == 'modified':
                modified = str(value)
            if str(key) == 'language':
                language = str(value)
            if str(key) == 'format':
                format = str(value)
            if str(key) == 'publisher':
                publisher = str(value)
            if str(key) == 'width':
                width = str(value)
            if str(key) == 'height':
                height = str(value)

        pot.node("file_info", "CMAP Information\n\n" + '\lTitle:\t'+title+'\lCreated:\t'+
                 created+'\lModified:\t'+modified+'\lLanguage:\t'+language+'\lFormat:\t'+
                 format+'\lPublisher:\t'+publisher+'\lWidth:\t'+width+'\lHeight:\t'+height+'\l',style='filled',fillcolor='#E6E6FA', shape='tab',Gsplines='true', fontsize = fr_s)
    nm_student = name(e)
    nm_instructor = name(a)

    if (isView == True):
        pot.render('results/' + str(nm_student) +"/"+str(nm_student)+ "- " +str(nm_instructor)+'_only' + '.gv', view=True)
        dot.render('results/' + str(nm_student) +"/"+str(nm_student)+ "- " +str(nm_instructor)+'.gv', view=True)
    else:
        pot.render('results/' + str(nm_student) + "/" + str(nm_student) + "- " + str(nm_instructor) + '_only' + '.gv',
                   view=False)
        dot.render('results/' + str(nm_student) + "/" + str(nm_student) + "- " + str(nm_instructor) + '.gv', view=False)
    end = time.process_time()
    M = round(end - start, 2)
    if (not isinstance(a, str)) and (not isinstance(a, list)):
        print(str(type(a)) + " " + str(a) + " is not accepted")
    if (not isinstance(e, str)) and (not isinstance(e, list)):
        print(str(type(e)) + " " + str(e) + " is not accepted")
    if isinstance(a, list):
        end = 0
        for i in a:
            if not i.endswith('.cxl'):
                end += 1
        if end > 0:
            print(str(a) + ' are not *.cxl files\n')
    if isinstance(e, list):
        end = 0
        for i in e:
            if not i.endswith('.cxl'):
                end += 1
        if end > 0:
            print(str(e) + ' are not *.cxl files\n')
    if isinstance(a, str):
        if not a.endswith('.cxl'):
            print(str(a) + ' is not a *.cxl file')
    if isinstance(e, str):
        if not e.endswith('.cxl'):
            print(str(e) + ' is not a *.cxl file')

    return A,B,C,D,E,F,G,H,I,J,K,L,M


def main():
    a = r'ConceptMapFiles\CXLFiles\ComputerSecurity\Instructor\Module1IntroductionComputerSecurity\Lesson1ComputerSecurityOverview\CS_Overview.cmap.cxl'
    b = r'ConceptMapFiles\CXLFiles\ComputerSecurity\Student\Module1IntroductionComputerSecurity\ICSAnonymous6.cmap.cxl'

    n = len(sys.argv)

    if (n > 1):
        a = str(sys.argv[1])
    if (n > 2):
        b = str(sys.argv[2])

    dia(a, b,0.3,0.3,0.3,30)

    # excel('UA_Overview.cmap.cxl', r'ConceptMapFiles\CXLFiles\ComputerSecurity\Student\Module2UserAuthentication')

def excel(a: str,e:str) -> 0:
    """
    :return a excel file for n number of student from a directory and a instructor concept map
    """
    if os.path.isdir(e) and os.path.isfile(a):
        current_directory = os.getcwd()
        onlyfiles = [f for f in listdir(e) if isfile(join(e, f))]
        print(onlyfiles)
        final_directory = os.path.join(current_directory, r'Excel_data')
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)
        nm_instructor = name(a)
        workbook = xlsxwriter.Workbook('Excel_data/' + str(nm_instructor) + ' ' + str(time.time()) + '.xlsx')
        worksheet = workbook.add_worksheet()
        worksheet.write('A1', 'Student')
        worksheet.write('B1', 'Matched B.')
        worksheet.write('C1', 'Partial B.')
        worksheet.write('D1', 'Mismatched B.')
        worksheet.write('E1', 'Extra B.')
        worksheet.write('F1', 'Total M.')
        worksheet.write('G1', 'Concept M.')
        worksheet.write('H1', 'LP M.')
        worksheet.write('I1', 'Misconcep.')
        worksheet.write('J1', 'Hier. M.')
        worksheet.write('K1', 'Grade')
        worksheet.write('L1', 'Element')
        worksheet.write('M1', 'Time(sec)')
        # Directory
        n = 0
        for i in onlyfiles:
            if os.path.exists(e) and str(i).endswith('.cxl'):
                n+=1
                A, B, C, D, E, F, G, H, I, J, K, L, M = dia(a, e+'\\'+str(i), False)
                worksheet.write('A' + str(n + 1), A)
                worksheet.write('B' + str(n + 1), B)
                worksheet.write('C' + str(n + 1), C)
                worksheet.write('D' + str(n + 1), D)
                worksheet.write('E' + str(n + 1), E)
                worksheet.write('F' + str(n + 1), F)
                worksheet.write('G' + str(n + 1), G)
                worksheet.write('H' + str(n + 1), H)
                worksheet.write('I' + str(n + 1), I)
                worksheet.write('J' + str(n + 1), J)
                worksheet.write('K' + str(n + 1), K)
                worksheet.write('L' + str(n + 1), L)
                worksheet.write('M' + str(n + 1), M)
        workbook.close()
    return 0
if __name__ == '__main__':
    main()
