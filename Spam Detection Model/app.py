import streamlit as st
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






st.title('Email / SMS Spam Detection')
input_text = st.text_area('Please provide me the input')




if st.button('Predict'):
   text_sms = text_transform(input_text)
   vectorize_text = tfidf.transform([text_sms])
   prediction = model.predict(vectorize_text)[0]

   if prediction == 1:
      st.header('This is a Spam Message')
   else:
      st.header("You're Good to Go")

 