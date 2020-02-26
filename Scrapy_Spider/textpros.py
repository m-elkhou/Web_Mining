import re, csv
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
import pandas as pd
import numpy as np
from PIL import Image
# import gensim
# from gensim import corpora,models
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from wordcloud import WordCloud

import arabic_reshaper
from bidi.algorithm import get_display
class textPros:

    def __init__(self):
        self.stemmer = PorterStemmer()
        self.stop_words = stopwords.words('arabic')
        self.stop_words.extend(stopwords.words('french'))
        self.stop_words.extend(stopwords.words('english'))
        with open("arabic_stop_words.txt","r", newline="",encoding="utf-8") as f:        
            for l in f:
                l = re.sub(r"\n+","",l)
                self.stop_words.append(l)
        self.stop_words.extend(['tout','le','la'])

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

    def plot(self, csv_path = "outputfile.csv"):
        csv_path = "outputfile.csv"
        df = pd.read_csv(csv_path)
        comments_list=[]
        type_list = df['type'].unique()
        for article_type in type_list:
            comments = df[df['type']==article_type]['comments_2']
            all_comments = " ".join(comments)
            all_comments = get_display(arabic_reshaper.reshape(all_comments))
            comments_list.append(all_comments)


            # mask = np.array(Image.open('black-cloud.png'))
            # wc = WordCloud(
            #     font_path='arial',
            #     background_color="white",
            #     mode='RGB',
            #     mask = mask,
            #     max_words=2000,
            #     width = 1024,
            #     height = 720,
            #     stopwords = self.stop_words
            # )

            # # # Generate the cloud
            # # wc.generate_from_frequencies(weights)
            # wc.generate(all_comments)

            # # Save the could to a file
            # wc.to_file("word_cloud.png")

            # plt.title(article_type)
            # plt.imshow(wc)
            # plt.axis("off")
            # plt.show()
            # # break
    

        tokens = [[token for token in doc.lower().split() ] for doc in comments_list]
        # print(tokens)
        dict = Dictionary(tokens)
        corpus_doc2bow_vectors = [dict.doc2bow(tok_doc) for tok_doc in tokens]
        # tfidf_model = TfidfModel(corpus_doc2bow_vectors, id2word=dict, normalize=False)
        tfidf_model = TfidfModel(corpus_doc2bow_vectors)

        for i in range(len(comments_list)):
            corpus_tfidf_vectors = tfidf_model[corpus_doc2bow_vectors[i]]
            # Get terms from the dictionary and pair with weights
            weights = {dict[pair[0]]: pair[1] for pair in corpus_tfidf_vectors}
            # weights = {get_display(arabic_reshaper.reshape(dict[pair[0]])): pair[1] for pair in corpus_tfidf_vectors}
            # Initialize the word cloud
            # print(weights)
            mask = np.array(Image.open('black-cloud.png'))
            wc = WordCloud(
                font_path='arial',
                background_color="white",
                mode='RGB',
                mask = mask,
                max_words=2000,
                width = 1024,
                height = 720,
                stopwords = self.stop_words
            )

            # # Generate the cloud
            wc.generate_from_frequencies(weights)

            # Save the could to a file
            wc.to_file("word_cloud.png")
            fig = plt.figure(i)
            plt.title(type_list[i])
            plt.imshow(wc)
            plt.axis("off")
            fig.show()
            plt.show()
            # break

textPros().plot()