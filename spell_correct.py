from data import MovieDataRetriever
data_retriever = MovieDataRetriever()
df = data_retriever.get_data()
from textblob import TextBlob
def correct_spells(s):
    textblb = TextBlob(s)
    return textblb.correct().string


df['desc_spell_corr'] = df['description'].apply(correct_spells)
print(df[['desc_spell_corr', 'description']])