from data import MovieDataRetriever
data_retriever = MovieDataRetriever()
df = data_retriever.get_data()

## Lowercasing
print(df['description'].str.lower())

## Remove url
# No text stars with http or www

## Remove punctuation
import string
print(string.punctuation)

        