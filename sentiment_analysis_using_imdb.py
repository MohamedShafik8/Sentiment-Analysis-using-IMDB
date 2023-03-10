# -*- coding: utf-8 -*-
"""Sentiment Analysis using IMDB.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rhuBEsCk6PUpqlWG3XRrfCaZOqNeYo3m
"""

import numpy as np
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from numpy import array,asarray
import seaborn as s
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers.core import Activation,Dropout,Dense
from keras.layers import Flatten,GlobalMaxPooling1D
from keras.layers import Embedding
from keras.preprocessing.text import one_hot
from sklearn.model_selection import train_test_split

import pandas as pd
movie_reviews= pd.read_csv('/content/IMDB Dataset.csv')
movie_reviews.head()

movie_reviews['review'][4]

def preprocess_text(sen):
  sentence=remove_tags(sen)
  sentence=re.sub('[^a-zA-Z]',' ',sentence)
  sentence=re.sub(r'\s+[a-zA-Z]\s+',' ',sentence)
  sentence=re.sub(r'\s+',' ',sentence)
  return sentence

import re
TAG_RE= re.compile(r'<[^>]+>')
def remove_tags(text):
  return TAG_RE.sub(' ',text)

review=[]
sentences=list(movie_reviews['review'])
for sen in sentences:
  review.append(preprocess_text(sen))

review[4]

from numpy import array
converted=movie_reviews['sentiment']
converted=np.array(list(map(lambda x:1 if x=='positive' else 0, converted)))

s.countplot(x='sentiment',data=movie_reviews)

review_train,review_test,converted_train,converted_test=train_test_split(review,converted,test_size=0.2,random_state=42)

tokenizer= Tokenizer(num_words=5000)
tokenizer.fit_on_texts(review_train)
review_train=tokenizer.texts_to_sequences(review_train)
review_test=tokenizer.texts_to_sequences(review_test)

vocab_size=len(tokenizer.word_index)+1
maxlen=100
review_train=pad_sequences(review_train,padding='post',maxlen=maxlen)
review_test=pad_sequences(review_test,padding='post',maxlen=maxlen)

from numpy import asarray,zeros
embedding_dictionary=dict()
glove_file=open("/content/glove.6B.100d.txt",encoding='utf8')

for line in glove_file:
  records=line.split()
  word=records[0]
  vector_dimensions=asarray(records[1:],dtype='float32')
  embedding_dictionary[word]=vector_dimensions
glove_file.close()

embedding_matrix=zeros((vocab_size,100))
for word,index in tokenizer.word_index.items():
  embedding_vector=embedding_dictionary.get(word)
  if embedding_vector is not None:
    embedding_matrix[index]=embedding_vector

from keras.layers import LSTM
model= Sequential()
model.add(Embedding(vocab_size,100,trainable=False,weights=[embedding_matrix],input_length=maxlen))
model.add(LSTM(128))
model.add(Dense(1,activation='sigmoid'))
model.summary()
model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['acc'])

history=model.fit(review_train,converted_train,batch_size=128,epochs=5,verbose=1,validation_split=0.2)

score=model.evaluate(review_test,converted_test,verbose=1)
print('Test score:', score[0])
print('Test accuracy:', score[1])

instance=review[98]
print(instance)

instance=tokenizer.texts_to_sequences(instance)
flat_list=[]
for sublist in instance:
  for item in sublist:
    flat_list.append(item)
flat_list=[flat_list]
instance=pad_sequences(flat_list,padding='post',maxlen=maxlen)
model.predict(instance)

plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model_accuracy')
plt.xlabel('epoch')
plt.ylabel('accuracy')
plt.legend(['train','test'],loc='upper left')
plt.show()

