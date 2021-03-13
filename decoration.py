"""
Copyright 2020, Masrik Dahir, All Right Reserved
"""
import pathlib
import webbrowser
import pandas as pd
import reform
import xmlPursing
import pdfkit
import os


def getDf(ins:dict) -> pd:
    """
    :return dataframe from dictionary
    """
    pd.set_option('display.max_rows', len(ins))
    df = pd.DataFrame.from_dict(ins, orient='index')
    node = 1
    lp = 1
    for i in df.keys()[0:]:
        if i % 2 == 0:
            df = df.rename(columns={i: "Node " + str(node)})
            node += 1
        else:
            df = df.rename(columns={i: "Linking Phrase " + str(lp)})
            lp += 1
    return df


def setDefault(ins: dict) -> pd:
    """
    :return the default styler for every dataframe
    """
    pd.set_option('display.max_rows', len(ins))
    df = pd.DataFrame.from_dict(ins, orient='index')
    node = 1
    lp = 1
    for i in df.keys()[0:]:
        if i % 2 == 0:
            df = df.rename(columns={i: "Node " + str(node)})
            node += 1
        else:
            df = df.rename(columns={i: "Linking Phrase " + str(lp)})
            lp += 1

    s = df.style.set_properties(**{'background-color': 'beige',
                               'color': 'black',
                               'border-color': 'black',
                               'border-width': '2px',
                               'border-style': 'solid'})
    return s

def highlight(val:str) -> pd:
    """
    highlight the missed concepts and linking phrases in red
    """
    color = None

    if ' #$#' in val:
        color = '#FFB6C1'
    elif val == '':
        color = 'white'
    return 'background-color: %s' % color


def result(ins:dict) -> pd:
    """
    color hte dataframe with CSS property properly
    """
    df = getDf(ins)
    df = df.fillna(value='')
    df2 = df
    unique = df.style.set_properties(**{'background-color': 'greenyellow',
                               'color': 'black',
                               'border-color': 'black',
                               'border-width': '2px',
                               'border-style': 'solid',
                                'text-align': 'center',
                                'table text-align' : 'center',
                                'text': 'asd'})

    s = unique.applymap(highlight)
    for i in df.columns.tolist():
        s.format({i: lambda x: x.replace(' #$#', '')})

    return s

def toPdf(ins_directory:str ,stu_directory: str, isView:bool = True) -> None:
    """
    generate a PDF to show the dataframe
    """
    ins = xmlPursing.process(ins_directory)
    stu = xmlPursing.process(stu_directory)
    diff = reform.ndict(ins, stu)
    nm_student = name(stu_directory)
    nm_instructor = name(ins_directory)
    styled_df = result(ins)
    html = styled_df.hide_index().render()
    with open('results/'+str(nm_student) + "/"+str(nm_student)+ "-" +str(nm_instructor) + "oo7.html", "w") as fp:
        fp.write(html)
    pdfkit.from_file('results/'+str(nm_student) + "/"+str(nm_student)+ "-" +str(nm_instructor)+ 'oo7.html', 'results/'+str(nm_student) + "/"+str(nm_student)+ "-" +str(nm_instructor) + '.pdf')

    if isView == True:
        webbrowser.get('windows-default').open_new_tab(r'file:///'+str(pathlib.Path().absolute()).replace('\\','/')+'/results/'+str(nm_student) + '/'+str(nm_student)+ '-' +str(nm_instructor) + '.pdf')
    if os.path.exists('results/'+str(nm_student) + "/"+str(nm_student)+ "-" +str(nm_instructor) + 'oo7.html'):
        os.remove('results/'+str(nm_student) + "/"+str(nm_student)+ "-" +str(nm_instructor) + 'oo7.html')


def toHtml(ins_directory:str, stu_directory:str) -> None:
    """
    generate a HTML to portray the dataframe
    """
    ins = xmlPursing.process(ins_directory)
    stu = xmlPursing.process(stu_directory)
    diff = reform.ndict(ins, stu)
    nm_student = name(stu_directory)
    nm_instructor = name(ins_directory)
    styled_df = result(ins)
    html = styled_df.hide_index().render()
    with open('results/'+str(nm_student) + "/"+str(nm_student)+ "-" +str(nm_instructor)+".html", "w") as fp:
        fp.write(html)

def name(stu: str or list) -> str:
    """
    :return the name of the file from a directory
    """
    li = []
    nm = None
    if isinstance(stu, str):
        li = stu.split('\\')
    if isinstance(stu, list):
        li = stu[len(stu) - 1].split('\\')
    nm = li[len(li) - 1].replace('.cxl', '').replace('.cmap', '')
    return nm

def main():
    a = 'CS_Overview.cmap.cxl'
    b = 'CS_CIA_Triad.cmap.cxl'
    c = 'CS_Relationships.cmap.cxl'
    d = 'CS_Terms.cmap.cxl'
    e = 'ICSAnonymous1.cmap.cxl'
    f = 'ConceptMapFiles\CXLFiles\ComputerSecurity\Student\Module1IntroductionComputerSecurity\ICSAnonymous1.cmap.cxl'
    toPdf(a, f)


if __name__ == "__main__":
    main()
