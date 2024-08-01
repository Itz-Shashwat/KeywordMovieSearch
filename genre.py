import requests 
from flask import Flask, request, jsonify
from flask_cors import CORS

host = Flask(__name__)
CORS(host)
API_KEY = "c927a8c2"

class OMDB:
    @staticmethod
    def get_top_movies_by_genre(genre):
        gen = genre
        keyword = gen
        response = requests.get(f'http://www.omdbapi.com/?apikey={API_KEY}&s={keyword}&type=movie')
        movies = response.json().get('Search', [])
        sorted_movies = sorted(movies, key=lambda x: float(x.get('imdbRating', 0)), reverse=True)
        return sorted_movies[:10]

@host.route('/', methods=['GET'])
def get_top_movies():
    genre = request.args.get('genre', '')
    if not genre:
        return jsonify({'error': 'Please provide a genre.'}), 400
    
    top_movies = OMDB.get_top_movies_by_genre(genre)
    return jsonify(top_movies)

if __name__ == '__main__':
    host.run(debug=True)
