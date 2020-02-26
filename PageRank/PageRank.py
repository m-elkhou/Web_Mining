import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET

def PageRank( M, dmp = 0.85, eps = 1.0e-5, max_iter = 100):
    """
    M : transation matrix
    dmp : Damping factor ; usually set to 0.85
    eps : Pre-specified threshold (desired precision); //used in Stopping condition
    max_iter : Maximum number of iterations
    """
    nb_site = len (M)
    R_old = [1/nb_site for _ in range(nb_site)]
    cpp = 0
    while True:
        R = M.dot(R_old)
        R = [ (1-dmp)/nb_site + dmp*r for r in R]

        flag = True
        for r1, r2 in zip(R, R_old):
            if abs(r1 - r2) > eps:
                flag = False
                break

        if flag or cpp >= max_iter:
            break

        R_old = R
        cpp+=1

    return cpp, R

# A = np.array([[   0,  0 , 1, 1/2], 
#               [ 1/3,   0, 0,   0], 
#               [ 1/3, 1/2, 0, 1/2], 
#               [ 1/3, 1/2, 0,   0]])
# eps = 0.00001
# nb_etr = 100

# print(PageRank(A, eps = eps, max_iter= 100))

def pagerank( G, dmp = 0.85, eps = 1.0e-5, max_iter = 100):
    """
    PageRank computes a ranking of the nodes in the graph G based on 
    the structure of the incoming links. It was originally designed as 
    an algorithm to rank web pages. 
  
    Parameters 
    ---------- 
    G           : xml path of graph
    M           : transation matrix; The adjacency matrix of the web graph
    dmp         : damping factor ; usually set to 0.85
    eps         : Pre-specified threshold (desired precision); used in Stopping condition
    max_iter    : Maximum number of iterations               ; used in Stopping condition

    Returns 
    ------- 
    pagerank : dictionary; Dictionary of nodes with PageRank as value
    """
    graph = ET.parse(G).getroot()
    nb_site = len(graph)

    # kt7wwl l graph mn xml l dictionary 
    link_dict ={}
    for i,node in enumerate(graph):
        link_dict[node.get("link")] =[ i, [link.get('value') for link in node] ]
    print(link_dict)
    # {'page1': [0, ['page2', 'page3', 'page4']],
    #  'page2': [1, ['page3', 'page4']],
    #  'page3': [2, ['page1']],
    #  'page4': [3, ['page3', 'page1']]}

    # dictionary 2 translation matrix
    M = [[0 for _ in range(nb_site)] for _ in range(nb_site)] # transation matrix
    for i,node in enumerate(link_dict):
        for link in link_dict[node][1]:
            M[link_dict[link][0]][link_dict[node][0]] = 1/len(link_dict[node][1])
    M = np.array(M)
    print(M)
    # [[0.         0.         1.         0.5       ]
    #  [0.33333333 0.         0.         0.        ]
    #  [0.33333333 0.5        0.         0.5       ]
    #  [0.33333333 0.5        0.         0.        ]]

    R_old = [1/nb_site for _ in range(nb_site)]
    cpp = 0
    while True:
        R = M.dot(R_old)
        R = [ (1-dmp)/nb_site + dmp*r for r in R]

        flag = True
        for r1, r2 in zip(R, R_old):
            if abs(r1 - r2) > eps:
                flag = False
                break

        if flag or cpp >= max_iter: # Stopping condition
            break

        R_old = R   # update
        cpp+=1

    print(cpp)
    return {'id':list(range(nb_site)), 'link': list(link_dict), 'rank': R}

home =  ''
dict1 = pagerank(home+'graph1.xml')
df = pd.DataFrame(dict1)
df.sort_values(by=['rank'], ascending=False, inplace=True)
df.reset_index(drop=True,inplace=True)
print(df)