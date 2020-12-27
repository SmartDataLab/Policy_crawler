#%%
"""
To csv format for submission
"""
import pymongo
import pandas as pd

MONGO_URI = 'mongodb://localhost:27017'
MONGO_DB = 'Policy'
COLLECTION = 'sample_task'

client = pymongo.MongoClient(MONGO_URI)
db  = client[MONGO_DB]
table = db[COLLECTION]
data_list = list(table.find())
client.close()
df = pd.DataFrame(data_list)

df.to_csv('../../data/raw_data.csv')

# %%
"""
Data clean & Partition
"""
import pickle
import re
import jieba
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
doc_list = []
for piece in data_list:
    words_per_doc = []
    for paragraph in piece['mainText']:
        sub_paragraph = re.sub(\
            "[0-9\s+\.\!\/_,$%^*()?;；:-【】+\"\']+|[+——！，;:。？、~@#￥%……&*（）]+",\
            ' ',paragraph)
        words_per_doc += jieba.lcut(sub_paragraph)
    doc_list.append(' '.join(words_per_doc))

#%%
"""
Prepare data to plot wordcloud
"""
CV = CountVectorizer(token_pattern='\\b\\w+\\b')
CV.fit_transform(doc_list)
word_count = CV.vocabulary_

with open('../../data/word_cloud.pk','wb') as f:
    pickle.dump(word_count,f)

# %%
import numpy
cv_count = CountVectorizer(token_pattern='\\b\\w+\\b').fit_transform(doc_list)
tf_transformer = TfidfTransformer(use_idf=True)
tf_idf = tf_transformer.fit_transform(cv_count)
print(tf_idf.shape)

with open('../../data/tf_idf.pk','wb') as f:
    pickle.dump(tf_idf,f)

# %%
with open('../../data/doc_list.pk','wb') as f:
    pickle.dump(doc_list,f)


# %%
