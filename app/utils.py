import requests
from dotenv import load_dotenv
import os

load_dotenv()

class Utils:

    @staticmethod
    def fetch_and_prepare_item_data(item_id, category):
        result = ApiRequest.get_api_details(item_id, category)
        if result:
            return {
                "category": category,
                "api_id": result.get("api_id"),
                "title": result.get("title"),
                "image": result.get("image"),
                "description": result.get("description"),
                "release_year": result.get("release_year"),
                "grade": result.get("grade"),
                "additional_info": result.get("additional_info", {}),
            }
        return None

    @staticmethod
    def get_item_type(category_type):
        return 'task' if category_type == 'todo_list' else 'item'

    @staticmethod
    def format_release_date(date_str):
        if not date_str:
            return "Unknown"
        try:
            return date_str.split('-')[0]
        except ValueError:
            return date_str

    @staticmethod
    def format_title(title, original_title):
        formated_title = title
        if original_title and original_title != title:
            formated_title = f"{title} ({original_title})"
        return formated_title

class ApiRequest:

    @staticmethod
    def fetch_animes(base_url, query):
        clientId = os.environ.get('CLIENT_ID_ANIMELIST')
        query = "'" + query + "'"
        fields = "id,title,synopsis,mean,start_date,end_date,num_episodes"
        url = '{}?q={}&limit={}&fields={}'.format(base_url, query, 5, fields)
        headers = {
            "X-MAL-CLIENT-ID": clientId
        }
        response = requests.get(url, headers=headers)
        if response and response.status_code == 200:
            json_data = response.json()
            results = json_data.get('data', json_data)
            animes = []
            for current_anime in results:
                result = {}
                current_anime = current_anime.get('node')
                result['api_id'] = current_anime.get('id')
                result['title'] = current_anime.get('title')
                result['description'] = current_anime.get('synopsis')
                result['grade'] = current_anime.get('mean', 0)
                result['release_year'] = Utils.format_release_date(current_anime.get('start_date'))
                result['image'] = current_anime.get('main_picture', {}).get('large')
                animes.append(result)
            return animes
        return []

    @staticmethod
    def fetch_anime_details(item_id, base_url):
        clientId = os.environ.get('API_KEY_ANIMELIST')
        fields = "id,title,synopsis,mean,start_date,end_date,num_episodes"
        url = '{}/{}?fields={}'.format(base_url, item_id, fields)
        headers = {
            "X-MAL-CLIENT-ID": clientId
        }
        response = requests.get(url, headers=headers)
        if response and response.status_code == 200:
            json_data = response.json()
            data = json_data.get('data', json_data)
            anime = {
                'api_id': data.get('id'),
                'title': data.get('title'),
                'description': data.get('synopsis'),
                'image': data.get('main_picture', {}).get('large'),
                'grade': data.get('mean', 0),
                'release_year': Utils.format_release_date(data.get('start_date')),
            }
            return anime
        return None

    @staticmethod
    def fetch_movies(base_url, query):
        url = "{}/search/movie?query={}".format(base_url, query)
        headers = {
            'Authorization': 'Bearer {}'.format(os.environ.get('CLIENT_ID_MOVIE_DB'))
        }

        response = requests.get(url, headers=headers)
        if response and response.status_code == 200:
            json_data = response.json()
            results = json_data.get('results', json_data)
            limited_results = results[:5]
            movies = []
            
            for current_movie in limited_results:
                result = {}
                result['api_id'] = current_movie.get('id')
                result['title'] = Utils.format_title(current_movie.get('title'), current_movie.get('original_title'))
                result['description'] = current_movie.get('overview')
                result['image'] = "https://image.tmdb.org/t/p/w500" + str(current_movie.get('poster_path'))
                result['grade'] = current_movie.get('vote_average')
                result['release_year'] = Utils.format_release_date(current_movie.get('release_date'))
                movies.append(result)
            return movies
        return []

    @staticmethod
    def fetch_movie_details(item_id, base_url):
        url = base_url + '/movie/{}'.format(item_id)
        headers = {
            'Authorization': 'Bearer {}'.format(os.environ.get('CLIENT_ID_MOVIE_DB'))
        }
        response = requests.get(url, headers=headers)
        if response and response.status_code == 200:
            json_data = response.json()
            results = json_data.get('results', json_data)
            movie = {
                'api_id': results.get('id'),
                'title': results.get('title'),
                'description': results.get('overview'),
                'image': "https://image.tmdb.org/t/p/w500" + str(results.get('poster_path')),
                'grade': results.get('vote_average'),
                'release_year': Utils.format_release_date(results.get('release_date')),
            }
            print(movie)
            return movie
        return None

    @staticmethod
    def fetch_tv_shows(base_url, query):
        url = "{}/search/tv?query={}".format(base_url, query)
        headers = {
            'Authorization': 'Bearer {}'.format(os.environ.get('CLIENT_ID_MOVIE_DB'))
        }
        response = requests.get(url, headers=headers)
        if response and response.status_code == 200:
            json_data = response.json()
            results = json_data.get('results', json_data)
            limited_results = results[:5]
            tv_shows = []

            for current_tv_show in limited_results:
                result = {}
                result['api_id'] = current_tv_show.get('id')
                result['title'] = Utils.format_title(current_tv_show.get('name'), current_tv_show.get('original_name'))
                result['description'] = current_tv_show.get('overview')
                result['image'] = "https://image.tmdb.org/t/p/w500" + str(current_tv_show.get('poster_path'))
                result['grade'] = current_tv_show.get('vote_average')
                result['release_year'] = Utils.format_release_date(current_tv_show.get('first_air_date'))
                tv_shows.append(result)
            return tv_shows
        return []

    @staticmethod
    def fetch_tv_show_details(item_id, base_url):
        url = '{}/tv/{}'.format(base_url, item_id)
        headers = {
            'Authorization': 'Bearer {}'.format(os.environ.get('CLIENT_ID_MOVIE_DB'))
        }
        response = requests.get(url, headers=headers)
        if response and response.status_code == 200:
            json_data = response.json()
            results = json_data.get('results', json_data)
            tv_show = {
                'api_id': results.get('id'),
                'title': results.get('name'),
                'description': results.get('overview'),
                'image': "https://image.tmdb.org/t/p/w500" + str(results.get('poster_path')),
                'release_year': Utils.format_release_date(results.get('first_air_date')),
                'grade': results.get('vote_average'),
            }
            return tv_show
        return None

    @staticmethod
    def get_api_search(query, category):
        base_url = category.get_api_url()
        category_type = category.type.lower()
        search_methods = {
            'movie': ApiRequest.fetch_movies,
            'anime': ApiRequest.fetch_animes,
            'tv_show': ApiRequest.fetch_tv_shows,
        }
        
        search_method = search_methods.get(category_type)
        if search_method:
            return search_method(base_url, query)
        return []

    @staticmethod
    def get_api_details(item_id, category):
        base_url = category.get_api_url()
        category_type = category.type.lower()
        search_methods = {
            'movie': ApiRequest.fetch_movie_details,
            'anime': ApiRequest.fetch_anime_details,
            'tv_show': ApiRequest.fetch_tv_show_details,
        }
        
        search_method = search_methods.get(category_type)
        if search_method:
            return search_method(item_id, base_url)
        return []
