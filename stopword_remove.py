from data import MovieDataRetriever
data_retriever = MovieDataRetriever()
df = data_retriever.get_data()

from nltk.corpus import stopwords
stopwords.words('english')