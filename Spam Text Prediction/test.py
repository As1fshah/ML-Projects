# import streamlit as st
import pickle
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
from nltk.corpus import stopwords
stopwords.words('english')
import string

def text_transform(text):


      text = text.lower()
      text = nltk.word_tokenize(text)

      y = []

      for i in text:
        if i.isalnum():
          y.append(i)


      text = y[:]
      y.clear()



      for i in text:
        if i not in stopwords.words('english') and string.punctuation:
          y.append(i)



      text = y[:]
      y.clear()


      for i in text:
        y.append(ps.stem(i))
      return ' '.join(y)



tfidf_path = 'tfid_vectorizer.pkl'
model_path = 'spam_text_detection_model.pkl'


tfidf = pickle.load(open(tfidf_path,'rb'))
model = pickle.load(open(model_path,'rb'))


def spam_detection_model(text):
  text = text_transform(text)
  text = tfidf.transform([text])
  result = model.predict(text)[0]
  return result


  
  





prediction = spam_detection_model("England v Macedonia - dont miss the goals/team news. Txt ur national team to 87077 eg ENGLAND to 87077 Try:WALES, SCOTLAND 4txt/Ì¼1.20 POBOXox36504W45WQ 16+")
if prediction == 1:
  print("Spam")
else:
   print('Not Spam')