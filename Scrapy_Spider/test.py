import re
from nltk.corpus import stopwords
stop_words = stopwords.words('arabic')
# with open("arabic_stop_words.txt","r", newline="",encoding="utf-8") as f:        
#     for l in f:
#         l = re.sub(r"\n+","",l)
#         stop_words.append(l)
# # print(stop_words)

# L = (1,2,3,4,"l")
# print(L.index("l"))



tweets=[['human', 'interface', 'computer'],
 ['survey', 'user', 'computer', 'system', 'response', 'time'],
 ['eps', 'user', 'interface', 'system'],
 ['system', 'human', 'system', 'eps'],
 ['user', 'response', 'time'],
 ['trees'],
 ['graph', 'trees'],
 ['graph', 'minors', 'trees'],
 ['graph', 'minors', 'survey']]
