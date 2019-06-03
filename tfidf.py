import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
import re
import requests

def dummy_fun(doc):
    return doc

class Tfidf:

    def __init__(self,passage,question):
        self.passage=passage
        self.question=question
        self.corpus=self.passage+self.question

    def getLemmasShallowParser(self,doc):

        headers = {
            'Referer': 'http://ltrc.iiit.ac.in/analyzer/kannada/',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'http://ltrc.iiit.ac.in',
            'Host': 'ltrc.iiit.ac.in',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Accept-Language': 'en-us',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Safari/604.1.38',
            'Content-Length': '630',
            'Upgrade-Insecure-Requests': '1',
        }

        data = {
          'input': doc.encode('utf-8'),
          'notation': 'utf',
          'out_notation': 'utf',
          'submit': 'Submit'
        }
        response = requests.post('http://ltrc.iiit.ac.in/analyzer/kannada/run.cgi', headers=headers, data=data)
        return response

    def parseLemmas(self,list):
        countParan=0
        countaf=0
        lemmatized=[]
        for token in list:
            if "((" in token:
                countParan+=1
            if countParan==1:
                if countaf==0:
                    if "af=" in token:
                        countaf+=1
                elif countaf>0:
                    if "af=" in token:
                        temp1=token.split("'")
                        temp2=temp1[1].split(",")
                        lemma=temp2[0]
                        if "." in lemma:
                            tempword=lemma.split(".")
                            lemmatized.append(tempword[0])
                            lemmatized.append(".")
                            lemmatized.append(tempword[1])
                        else:
                            lemmatized.append(lemma)
            if "))" in token:
                countParan=0
                countaf=0
            #if "----" in token:
                #lemmatized.append("eop")

        print(lemmatized)
        return lemmatized

    def getImportantWords(self,list):
        countparan=0
        countaf=0
        important=[]
        for token in list:
            if "((" in token:
                countparan+=1
            if countparan==1:
                if "NP" in token:
                    np+=1
                if np==1 and countaf==0:
                    if "af=" in token:
                        countaf+=1
                        temp1=token.split("'")
                        temp2=temp1[1].split(",")
                        lemma=temp2[0]
                        if "." in lemma:
                            tempword=lemma.split(".")
                            important.append(tempword[0])
                            important.append(".")
                            important.append(tempword[1])
                        else:
                            important.append(lemma)
                        important.append(lemma)
            elif "))" in token:
                    countparan=0
                    countaf=0
        return important
    def prepareTextforTfidf(self,corpus):
        texts=[]
        temp=[]

        f=open("stopwords.txt","r")
        stopwords=[]
        for i in f:
            stopwords.append(i.strip())
        #print(corpus)

        for word in corpus:
            if(word!="."):
                if (not re.fullmatch('[' + string.punctuation + ']+', word) and (not word in stopwords) and ((word and word.strip())) and len(word)>2 and word!="&gt;&nbsp&nbsp&nbsp&nbsp&nbsp</td>" and (not bool(re.search(r'\d', word))) and word!='oVMxu'):
                    temp.append(word)
            else:
                texts.append(temp)
                temp=[]
        texts.append(temp)
        return texts


    def tfidfCalculator(self):
    #preprocessing including tokenization and removal of punctuation
        corpus = nltk.sent_tokenize(self.corpus)
        docs=[]

        i=0
        templemmas=[]
        while i<=len(corpus)-1:
            temp=[]
            temp.append(corpus[i])
            if(i+1<=len(corpus)-1):
                temp.append(corpus[i+1])
            str1 = ""
            str2=str1.join(temp)
            shallowlemma=self.getLemmasShallowParser(str2)
            print(shallowlemma)
            for token in shallowlemma.text.split():
                    templemmas.append(token)
            i=i+2

        lemmas=self.parseLemmas(templemmas)
        cleanedlemmas=self.prepareTextforTfidf(lemmas)
        docs=cleanedlemmas

        #print(docs)
        tfidf = TfidfVectorizer(
            analyzer='word',
            tokenizer=dummy_fun,
            preprocessor=dummy_fun,
            token_pattern=None)

        tfidf.fit(docs)
        vec=tfidf.transform(docs)
        vocab=tfidf.vocabulary_
        vectors = [t for t in vec.toarray()]
        listofsim=cosine_similarity(vectors)
        print(listofsim)
        print(docs)
        simofans=listofsim[len(listofsim)-1]
        print(simofans)
        max=0
        index=0
        for i in range(0,len(simofans)-1):
            if max<simofans[i]:
                max=simofans[i]
                index=i
        print(corpus[index],index, corpus)
        upper=[]
        lower=[]
        i=0
        seen=0
        passage=nltk.sent_tokenize(self.passage)
        for sent in passage:
            #if i==len(corpus):
                #break
            if sent!=corpus[index]:
                if seen==0:
                    upper.append(sent)
                elif seen==1:
                    lower.append(sent)
            else:
                seen=1
                answer=corpus[index]
            i=i+1
        first=""
        for sent in upper:
            first+=sent
        last=""
        for sent in lower:
            last+=sent
        #getting 5 top tfidf words
        """
        feature_names = tfidf.get_feature_names()
        features=[]
        for i in range(0,len(docs)-2):
            for col in vec.nonzero()[1]:
                features.append([col,vec[i,col]])
        final_list = []

        for i in range(0, 5):
            max1 = 0
            j=0
            for sublist in features:
                if sublist[1] > max1:
                    max1 = sublist[1]
                    elem=features[j]
                j=j+1
            features.remove(elem)
            final_list.append(elem)
        summary=[]
        vocab=dict((v, k) for k, v in vocab.items())
        for index in final_list:
            summary.append((vocab[index[0]]))
        """

        summary=self.getImportantWords(lemmas)
        return answer,self.question,first,last,vec,listofsim,simofans
