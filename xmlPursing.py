"""
Copyright 2020, Masrik Dahir, All Right Reserved
"""

import pprint
import xml.dom.minidom
import xml.etree.ElementTree as ET
import re

nodes = {}
linking = {}
connection = {}
from_Id = {}
to_Id = {}
idConnection = {}
branch = {}

first = []
second = []
new_list = []
listBranch = []
final = []

n = 0
def information(File: str) -> dict:
    """
    :return basic information of the student concept map
    """
    dict = {}
    tree = ET.parse(File)
    root = tree.getroot()
    for i in range(0, len(root[0])-1):
        key = root[0][i].tag
        f_ind = key.index('{')
        l_ind = key.index('}')
        s = key[l_ind+1:]
        dict[s] = root[0][i].text
    new_dict = {}
    for i in root:
        if len(i.attrib) != 0:
            new_dict = i.attrib
    dict.update(new_dict)
    return dict


def main():
    a = 'CS_Overview.cmap.cxl'
    b = 'CS_CIA_Triad.cmap.cxl'
    c = 'CS_Relationships.cmap.cxl'
    d = 'CS_Terms.cmap.cxl'
    e = 'ICSAnonymous1.cmap.cxl'
    print(process(b))
    print(orphan_list([b]))
    print(information(a))


def process(File: str, n: int = 0) -> dict:
    """
    process all the other function and return a newly formed and sorted dictionary
    the parameter n is only important when inputting multiple CXL file to get a combined dictionary
    """
    branch_f = {}
    form_dictionary(File)
    orphan = find_orphan(idConnection)
    orphan.sort()
    branch_f.update(find_branch(orphan, n))
    return branch_f
def num_orphan(File: str, n: int = 0) -> int:
    """
    :return the number of orphrans
    """
    branch_f = {}
    form_dictionary(File)
    orphan = find_orphan(idConnection)
    return len(orphan)

def process_multiple (Files: list, n: int = 0) -> dict:
    """
    process all the other function and return a newly formed and sorted dictionary
    the parameter n is only important when inputting multiple CXL file to get a combined dictionary
    """
    branch_f = {}
    for File in Files:
        form_dictionary(File)
        orphan = find_orphan(idConnection)
        orphan.sort()
        branch_f.update(find_branch(orphan, len(branch_f)))
    return branch_f

def process_key(File: str, n: int = 0) -> dict:
    """
    process all the other function and return a newly formed and sorted dictionary
    the parameter n is only important when inputting multiple CXL file to get a combined dictionary
    """
    branch_f = {}
    form_dictionary(File)
    orphan = find_orphan(idConnection)
    orphan.sort()
    branch_f.update(find_branch_key(orphan, n))
    return branch_f

def process_key_many(File: list, n: int = 0) -> dict:
    """
    process all the other function and return a newly formed and sorted dictionary
    the parameter n is only important when inputting multiple CXL file to get a combined dictionary
    """
    result = {}
    for i in File:
        a = process_key(i, len(result))
        result.update(a)
    return result

def format(File: str) -> str:
    """
    format the dictionary into a
    """
    branch = process(File)
    branch_format = pprint.pformat(branch)
    return branch_format

def combine(*files: str) -> dict:
    """
    combine several dictionaries together, accept the directory for the files only
    :rtype: object
    """
    result = {}
    for i in files:
        a = process(i,len(result))
        result.update(a)
    return result

def find_branch(orphan: list, n: int = 0) -> dict:
    """
    find the entire branch from a the orphan
    reverse the branch to make it chronological
    """
    branch.clear()
    for i in orphan:
        listBranch.clear()
        final.clear()
        listBranch.append(i)
        next = find_parent(i)
        n = n + 1
        while (next != None):
            listBranch.append(next)
            next = find_parent(next)
        del listBranch[-1]
        listBranch.reverse()
        for j in listBranch:
            final.append(str(get_value_any(j)))
        branch[n] = final.copy()

    return branch


def find_branch_key(orphan: list, n: int = 0) -> dict:
    """
    find the entire branch from a the orphan
    reverse the branch to make it chronological
    """
    branch.clear()
    for i in orphan:
        listBranch.clear()
        final.clear()
        listBranch.append(i)
        next = find_parent(i)
        n = n + 1
        while (next != None):
            listBranch.append(next)
            next = find_parent(next)
        del listBranch[-1]
        listBranch.reverse()
        for j in listBranch:
            final.append(j)
        branch[n] = final.copy()

    return branch
def form_dictionary(File: str):
    """
    the function form four dictionaries which are essential for rest of the function to work
    """
    doc = xml.dom.minidom.parse(File)
    tree = ET.parse(File)
    connectionList = doc.getElementsByTagName('connection')
    idConnectionList = doc.getElementsByTagName('connection')
    conceptList = doc.getElementsByTagName('concept')
    linkingList = doc.getElementsByTagName('linking-phrase')
    nodes.clear()
    linking.clear()
    connection.clear()
    idConnection.clear()

    for j in conceptList:
        res = re.sub(' +', ' ', str(j.attributes['label'].value).replace("\n", " ").replace("\r",""))
        nodes[str(j.attributes['id'].value)] = res

    for i in linkingList:
        res = re.sub(' +', ' ', str(i.attributes['label'].value).replace("\n", " ").replace("\r",""))
        linking[str(i.attributes['id'].value)] = res

    for i in connectionList:
        if str(i.attributes['from-id'].value) in nodes:
            fromId = str(nodes[str(i.attributes['from-id'].value)])
        else:
            fromId = str(linking[str(i.attributes['from-id'].value)])
        if str(i.attributes['to-id'].value) in nodes:
            toId = str(nodes[str(i.attributes['to-id'].value)])
        else:
            toId = str(linking[str(i.attributes['to-id'].value)])
        connection[str(i.attributes['id'].value)] = (fromId, toId)
    for i in idConnectionList:
        idConnection[str(i.attributes['id'].value)] = (
        str(i.attributes['from-id'].value), str(i.attributes['to-id'].value))

def id_dict(File: str) -> dict:
    """
    creates a dictionary of connection id
    """
    idConnection = {}
    doc = xml.dom.minidom.parse(File)
    tree = ET.parse(File)

    idConnectionList = doc.getElementsByTagName('connection')
    for i in idConnectionList:
        idConnection[str(i.attributes['id'].value)] = [
        str(i.attributes['from-id'].value), str(i.attributes['to-id'].value)]
    return idConnection
def orphan_list(File: str or list) -> dict:
    """
    :return the orphans in dictionary
    """
    node_list = []
    all_node_list = []
    diff = {}
    if (isinstance(File, str)):
        for key, value in node(File).items():
            all_node_list.append(value)
        for key, value in process(File).items():
            for concept in value:
                if concept in all_node_list:
                    node_list.append(concept)
        for key, value in node(File).items():
            if value not in node_list:
                diff[key] = value
    if (isinstance(File,list)):
        for key, value in node_multiple(File).items():
            all_node_list.append(value)
        for key, value in process_multiple(File).items():
            for concept in value:
                if concept in all_node_list:
                    node_list.append(concept)
        for key, value in node_multiple(File).items():
            if value not in node_list:
                diff[key] = value
    return  diff

def id_dict_multiple(File: list) -> dict:
    """
    :return the id connection of multiple concept maps
    """
    idConnection = {}
    for f in File:
        doc = xml.dom.minidom.parse(f)
        tree = ET.parse(f)

        idConnectionList = doc.getElementsByTagName('connection')
        for k in idConnectionList:
            idConnection[str(k.attributes['id'].value)] = [
            str(k.attributes['from-id'].value), str(k.attributes['to-id'].value)]
    return idConnection
def node(File: str) -> dict:
    """
    :return the nodes of the concept maps in dictionary
    """
    nodes = {}
    doc = xml.dom.minidom.parse(File)
    tree = ET.parse(File)
    conceptList = doc.getElementsByTagName('concept')
    for j in conceptList:
        res = re.sub(' +', ' ', str(j.attributes['label'].value).replace("\n", " "))
        nodes[str(j.attributes['id'].value)] = res
    return nodes
def node_multiple(Files: list) -> dict:
    """
    :return the nodes of the concept maps in dictionary for multiple concept maps
    """
    nodes ={}
    for File in Files:
        doc = xml.dom.minidom.parse(File)
        tree = ET.parse(File)
        conceptList = doc.getElementsByTagName('concept')
        for j in conceptList:
            res = re.sub(' +', ' ', str(j.attributes['label'].value).replace("\n", " "))
            nodes[str(j.attributes['id'].value)] = res
    return nodes
def lf_multiple (Files: list) -> dict:
    """
    :return the linking phrases in multiple dictionaries of concept maps
    """
    linking = {}
    for File in Files:
        doc = xml.dom.minidom.parse(File)
        tree = ET.parse(File)
        linkingList = doc.getElementsByTagName('linking-phrase')
        for i in linkingList:
            res = re.sub(' +', ' ', str(i.attributes['label'].value).replace("\n", " "))
            linking[str(i.attributes['id'].value)] = res
    return linking


def lf (File: str) -> dict:
    """
    :return the linking phrases in a dictionary of concept map
    """
    linking = {}
    doc = xml.dom.minidom.parse(File)
    tree = ET.parse(File)
    linkingList = doc.getElementsByTagName('linking-phrase')
    for i in linkingList:
        res = re.sub(' +', ' ', str(i.attributes['label'].value).replace("\n", " "))
        linking[str(i.attributes['id'].value)] = res
    return linking

def find_associate(val: str) -> str or None:
    """
    find associate id for an id
    """
    mainId = None
    fractions = []
    associate = None
    try:
        for key, value in idConnection.items():
            if val.endswith(value):
                mainId = key
        if mainId in idConnection:
            associate = str(from_Id.get(mainId))
        if val not in associate:
            return associate
        else:
            associate = str(to_Id.get(mainId))
            return (associate)
    except:
        return None

def find_parent(val: str) -> str or None:
    """
    retirn the parent id
    """
    mainId = None
    fractions = []
    associate = None
    try:
        for key, value in idConnection.items():
            if val.endswith(value):
                mainId = key
            else:
                associate = None
        if mainId in idConnection:
            associate = str(from_Id.get(mainId))
        if val not in associate:
            return associate
        for key, value in to_Id.items():
            if val == value:
                mainId = key
            else:
                associate = None
        if mainId in idConnection:
            associate = str(from_Id.get(mainId))
            if str(associate) == str(val):
                associate = None
            return str(associate)
        else:
            associate = None
    except:
        return None

def get_key(val: list, dictionary: dict) -> str:
    """
    return key from a dictionary if the given value matches
    """
    stat = None
    for key, value in dictionary.items():
        if (val) == value:
            stat = key
    return str(stat)

def find_orphan(dictionary: dict) -> list:
    """
    find the list of orphans from the dictionary
    """
    first.clear()
    second.clear()
    from_Id.clear()
    to_Id.clear()
    for key in dictionary:
        result = str(dictionary[key]).replace("(","").replace(")","")
        a = result.split(", ")
        first.append(a[0].replace("'",""))
        from_Id[str(key)] = a[0].replace("'","")
        to_Id[str(key)] = a[1].replace("'","")
        second.append(a[1].replace("'",""))
    return list(set(second).difference(first))

def get_value(key: str, dictionary: dict) -> list or None:
    """
    return the value if the key matches a key in dictionary
    """
    if key in dictionary:
        return dictionary.get(key)
    else:
        return None

def delete_element(key: str, dictionary: dict) -> dict:
    """
    delete an element from a dictionary
    """
    del dictionary[key]

def get_key_any(val: list) -> str:
    """
    return the key that matches either from-id or to-id dictionary of ids
    they have separate keys
    """
    stat = None
    if val in nodes.values():
        for key, value in nodes.items():
            if val == value:
                stat = key
    if val in linking.values():
        for key, value in linking.items():
            if val == value:
                stat = key
    return stat
def get_value_any(key: str) -> list or None:
    """
    get value from a key from a dictionary either from-id or to-id dictionary of ids
    """
    if key in nodes:
        return nodes.get(key)
    if key in linking:
        return linking.get(key)
    else:
        return None
def Cloning(li1: list) -> list:
    """
    clone a list
    """
    li_copy = li1[:]
    return li_copy
def clear():
    """
    clear the branch dictionary
    """
    branch.clear()


if __name__ == '__main__':
    main()
