from gensim import corpora, models
import pickle
with open('../../data/doc_list.pk','rb') as f:
    doc_list = pickle.load(f)

dictionary = corpora.Dictionary(words_ls)

corpus = [dictionary.doc2bow(words) for words in words_ls]

lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=10)

for topic in lda.print_topics(num_topics=4):
    print(topic)