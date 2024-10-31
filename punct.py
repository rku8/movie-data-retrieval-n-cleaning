import string
punctuation = string.punctuation
print(punctuation)

from data import MovieDataRetriever
data_retriever = MovieDataRetriever()
df = data_retriever.get_data()

print(df['description'])

def remove_punct(s):
    s = str(s)
    for punct in punctuation:
        if punct in s:
            s = s.replace(punct, ' ')
    return s.replace('  ', ' ')

def remove_punct_efficient(s):
    s = str(s)
    st = s.translate(str.maketrans('', '', punctuation))
    return st



df['desc_m'] = df['description'].apply(remove_punct_efficient)
print(df[['description', 'desc_m']])
