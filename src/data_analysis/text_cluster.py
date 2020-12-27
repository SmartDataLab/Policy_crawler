import pickle
with open('../../data/tfidf.pk','rb') as f:
    tfidf = pickle.load(f)
from sklearn.cluster import KMeans  
clf = KMeans(n_clusters=20)  
s = clf.fit(tfidf)