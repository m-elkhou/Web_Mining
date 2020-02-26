import re
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer

class textPros:

    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = stopwords.words('arabic')
        with open("arabic_stop_words.txt","r", newline="",encoding="utf-8") as f:        
            for l in f:
                l = re.sub(r"\n+","",l)
                self.stop_words.append(l)

    def text_pros(self, text):
        # result =[]
        # for line in text:
        #     line = self.tokenize_regex_punct_keep(line)
        #     result.append(line)
        # return " ".join(result)
        return self.tokenize_regex_punct_keep(text)
    
    def tokenize_regex_punct_keep(self, text):
        #delete all non words exept html tags
        text = re.sub('[^\w<>]',' ',text)
        #delete javascript tags
        text =re.sub('< *script*>.*?< *script*>',' ',text)
        #delete all html tags
        text = re.sub('<.*?>',' ',text)
        #delete numbers 
        text = re.sub("[0-9><,]+"," ",text)
        #delete reteur a la ligne
        text = re.sub(r"\n+"," ",text)
        #replace multiple spaces with one space
        text = re.sub(r"\s+"," ",text)
        #transfer text to lowercase
        text = text.lower() 
        # tokenaze text
        tokens = re.split(" ", text)
        # Remove stop words        
        tokens = [word for word in tokens if word not in self.stop_words]
        
        stems = [self.stemmer.stem(t) for t in tokens]
        return " ".join(stems)