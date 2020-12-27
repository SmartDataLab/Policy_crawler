#%%
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pickle
font = '/usr/share/fonts/华文楷体.ttf'

with open('../../data/word_cloud.pk','rb') as f:
    words = pickle.load(f)

wc=WordCloud(background_color='White',width=800,height=600,font_path=font,scale=64)
wc.generate_from_frequencies(words)

plt.imshow(wc)
plt.axis("off")
plt.savefig('../../figure/wordcloud.png')
plt.show()




# %%
