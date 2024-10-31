import os
import csv
import requests
import pandas  as pd
from dotenv import load_dotenv
from typing import Any

load_dotenv()
tmdb_api_key = os.getenv('TMDB_API_KEY')

LINK = 'https://api.themoviedb.org/3/discover/movie?api_key={tmdb_api_key}&primary_release_year={year}&page={page_number}&with_original_language={language}'

def save_data(movie_data, csv_file):
    try:
        keys = movie_data[0].keys()
        # Writing the list of dictionaries to a CSV file
        with open(csv_file, 'w', newline='') as f:
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writeheader()  # Write the header (column names)
            dict_writer.writerows(movie_data)  # Write the data (rows)
    except Exception as e:
        raise Exception("Error saving the file")


class MovieDataRetriever:
    def __init__(self, url: str = LINK, 
                 st_year: int = 2005, 
                 end_year: int = 2024, 
                 mx_page: int = 25,
                 language: str = "en",
                 filename: str = 'output.csv'):
        self.url = url
        self.start_year = st_year
        self.end_year = end_year
        self.max_page = mx_page
        self.language = language
        self.filename = filename
        self.genre_list = self._fetch_all_genre()
        self.movie_data = []

    def _fetch_all_genre(self):
        genre_link = f'https://api.themoviedb.org/3/genre/movie/list?api_key={tmdb_api_key}'
        response_genre = requests.get(genre_link)
        genre_list = response_genre.json()['genres']

        return {genre['id']: genre['name'] for genre in genre_list}
    
    def get_genres(self, genre_ids: list):
        return [self.genre_list[id] for id in genre_ids]

    
    def get_movie_attribute(self, movie: dict) -> dict:
        movie_attrs = {
            'title' : movie['original_title'],
            'description' : movie['overview'],
            'genre' : self.get_genres(movie['genre_ids'])
        }

        return movie_attrs
    
    def download_data(self) -> None:
        for year in range(self.start_year, self.end_year):
            for page_number in range(1, self.max_page):
                link = self.url.format(tmdb_api_key = tmdb_api_key, 
                                       year = year, 
                                       page_number = page_number, 
                                       language = self.language)
                response = requests.get(link)

                for movie in response.json()['results']:
                    self.movie_data.append(self.get_movie_attribute(movie))

        save_data(self.movie_data, self.filename)
        
    def get_data(self) -> Any:
        if not os.path.exists(self.filename):
                self.download_data()
        try:
            if len(self.movie_data) != 0:
                return pd.DataFrame(self.movie_data)
            elif os.path.exists(self.filename):
                return pd.read_csv(self.filename)
        except Exception as e:
            raise Exception("Error getting the data as dataframe")



if __name__=="__main__":
    data_reriever = MovieDataRetriever()
    data_reriever.download_data()
    df = data_reriever.get_data()
    print(df.head())
