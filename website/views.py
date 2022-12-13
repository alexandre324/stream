from flask import Blueprint, render_template, request, flash, jsonify
import json, random
from tinytag import TinyTag 
from sklearn.utils import shuffle

views = Blueprint('views', __name__)

def find_movies(searched_word, data, filters):
    movies = []
    for i in range(len(data)):
        movie = data.get(str(i))
        cathegorie = movie.get('filters')
        
        if searched_word in cathegorie:
            if filters == "random":
                if movie.get('type') == "film":
                    movies.append([movie.get('type'), i, movie.get('img'), movie.get('title'), movie.get('time'), str(movie.get('date')), movie.get('langage'), movie.get('url')])
                elif movie.get('type') == "serie":
                    movies.append(["serie", i, movie.get('img'), movie.get('title'), movie.get('langage'), movie.get('nbr_saisons')])
            elif filters == "films":
                if movie.get('type') == "film":
                    movies.append(["film", i, movie.get('img'), movie.get('title'), movie.get('time'), str(movie.get('date')), movie.get('langage'), movie.get('url')])
            elif filters == "serie":
                if movie.get('type') == "serie":
                    movies.append(["serie", i, movie.get('img'), movie.get('title'), movie.get('langage'), movie.get('nbr_saisons')])
            elif filters == "vo":
                if movie.get('langage') == "vo":
                    movies.append([movie.get('type'), i, movie.get('img'), movie.get('title'), movie.get('time'), str(movie.get('date')), "Vo", movie.get('url')])
            elif filters == "vf":
                if movie.get('langage') == "vf":
                    movies.append([movie.get('type'), i, movie.get('img'), movie.get('title'), movie.get('time'), str(movie.get('date')), "Vf", movie.get('url')])
        
    return movies

def import_movies(data, filters):
    movies = []
    for i in range(len(data)):
        movie = data.get(str(i))
        if filters == "random":
            if movie.get('type') == "film":
                movies.append([movie.get('type'), i, movie.get('img'), movie.get('title'), movie.get('time'), str(movie.get('date')), movie.get('langage'), movie.get('url')])
            elif movie.get('type') == "serie":
                movies.append(["serie", i, movie.get('img'), movie.get('title'), movie.get('langage'), movie.get('nbr_saisons')])
        elif filters == "films":
            if movie.get('type') == "film":
                movies.append(["film", i, movie.get('img'), movie.get('title'), movie.get('time'), str(movie.get('date')), movie.get('langage'), movie.get('url')])
        elif filters == "serie":
            if movie.get('type') == "serie":
                movies.append(["serie", i, movie.get('img'), movie.get('title'), movie.get('langage'), movie.get('nbr_saisons')])
        elif filters == "vo":
            if movie.get('langage') == "vo":
                movies.append([movie.get('type'), i, movie.get('img'), movie.get('title'), movie.get('time'), str(movie.get('date')), "Vo", movie.get('url')])
        elif filters == "vf":
            if movie.get('langage') == "vf":
                movies.append([movie.get('type'), i, movie.get('img'), movie.get('title'), movie.get('time'), str(movie.get('date')), "Vf", movie.get('url')])
    
    return shuffle(movies, random_state=random.randint(0, 40))

def format_word(word):
    new_string = ''.join(filter(str.isalnum, word))
    result = ''.join([i for i in new_string if not i.isdigit()])
    
    return result.lower()
    
def render_movies(filters):
    f = open('website/static/movies.json')
    data = json.load(f)

    search = ""
    
    if request.method == 'POST':
        search = request.form.get('search')
        Movies = find_movies(format_word(search), data, filters)

    else:
        Movies = import_movies(data, filters)

    for i in range(len(Movies)):
        if Movies[i][0] == "film":
            movie = ["watch", Movies[i][1], Movies[i][2], Movies[i][3], Movies[i][4], Movies[i][5], Movies[i][6], Movies[i][7], search]
        else:
            movie = ["episodes", Movies[i][1], Movies[i][2], Movies[i][3], Movies[i][4], Movies[i][5], search]
            print(movie)
                    
        flash(movie, category='x')

    f.close()

#home tab
@views.route('/', methods=['GET', 'POST'])
def home():
    render_movies("random")

    return render_template("home.html")

#film tab
@views.route('/films', methods=['GET', 'POST'])
def films():
    render_movies("films")
    
    return render_template("home.html")

#serie tab
@views.route('/serie', methods=['GET', 'POST'])
def serie():
    render_movies("serie")
    
    return render_template("home.html")

#film vf
@views.route('/vf', methods=['GET', 'POST'])
def vf():
    render_movies("vf")
    
    return render_template("home.html")

#film vo
@views.route('/vo', methods=['GET', 'POST'])
def vo():
    render_movies("vo")
    
    return render_template("home.html")

#watching page
@views.route('/watch', methods=['GET', 'POST'])
def watch():
    video_type = request.args.get('type', '') 
    if video_type == "film":
        movie_id = request.args.get('id', '') 
        f = open('website/static/movies.json')
        data = json.load(f)
        movie = data.get(str(movie_id))
        f.close()
        
        url = movie.get('url') 
        title = movie.get('title')

        movie_infos = [title, url]
    else:
        serie_id = request.args.get('id', '')
        serie_saison = int(request.args.get('saison', '')) - 1
        serie_episode = int(request.args.get('episode', ''))  - 1

        f = open('website/static/movies.json')
        data = json.load(f)
        serie = data.get(str(serie_id))
        saison = serie.get(str(serie_saison))
        episode = saison.get(str(serie_episode))
        print(episode)
        f.close()

        movie_infos = [episode.get("title"), episode.get("url")]

    flash(movie_infos, category='url')
    
    return render_template("watch.html")


#episode page
@views.route('/episodes', methods=['GET', 'POST'])
def episodes():
    movie_id = request.args.get('id', '') 
    f = open('website/static/movies.json')
    data = json.load(f)
    movie = data.get(str(movie_id))
    f.close()
    
    nbr_saisons = movie.get('nbr_saisons')
    serie_infos = [[movie_id]]

    for i in range(0, nbr_saisons):
        episodes = []

        saison_data = movie.get(str(i))
        nbr_episodes =  len(saison_data)
        
        for u in range(0, nbr_episodes - 1):
            episode_datas = saison_data.get(str(u))
            episodes.append([u, episode_datas.get("time"), episode_datas.get("title")])
        
        serie_infos.append(episodes)

    flash(serie_infos, category='url')

    return render_template("episodes.html")