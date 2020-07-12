from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from imdb_action.models import MovieStore
import json
from imdb_action.decorators import admin_required, api_login_required, http_response_smart

# Create your views here.

@csrf_exempt
@api_login_required
def get_all_movies(request):
    try:
        movie_data = MovieStore.objects.values('id','name', 'imdb_score', 'number_99popularity', 'genre', 'director')
        return HttpResponse(http_response_smart(list(movie_data), "Movie Data", "success"))
    except Exception as e:
        print(str(e))
        return HttpResponse(http_response_smart({}, "Error: " + str(e), "fail"), status = 403)


def build_filter(filter_map):
    kwargs = {}
    genre_list = []
    if len(filter_map.keys()) > 0:
        if "popularity" in filter_map.keys():
            kwargs['number_99popularity__gte'] = filter_map["popularity"]["value"]
        if "rating" in filter_map.keys():
            kwargs['imdb_score__gte'] = filter_map["rating"]["value"]
        if "director" in filter_map.keys():
            kwargs['director__icontains'] = filter_map["director"]["value"]
        if "name" in filter_map.keys():
            kwargs['name__icontains'] = filter_map["name"]["value"]
        if "genre" in filter_map.keys():
            genre_list = filter_map["genre"]["value"].split(",")
    return kwargs, genre_list


@csrf_exempt
@api_login_required
def search_movie(request):
    try:
        filter_map = request.POST.get('search_filter')
        if filter_map:
            filter_map_json = json.loads(filter_map)
            kwargs, genre_list = build_filter(filter_map_json)
            movie_data = MovieStore.objects.filter(**kwargs).all()
            if len(genre_list)>0:
                for genre in genre_list:
                    movie_data = movie_data.filter(genre__icontains=genre)
            movie_data = movie_data.values('id', 'name', 'imdb_score', 'number_99popularity', 'genre', 'director')
            return HttpResponse(http_response_smart(list(movie_data), "Movie Data", "success"), status=200)
        else:
            return HttpResponse(http_response_smart({}, "Parameter mismatch", "fail"), status=400)
    except Exception as e:
        print(str(e))
        return HttpResponse(http_response_smart({}, "Error: " + str(e), "fail"), status = 403)


@csrf_exempt
@api_login_required
def search_movie_by_name(request):
    try:
        name_regex = request.POST.get('name_regex')
        if name_regex:
            movie_data = MovieStore.objects.filter(name__icontains=name_regex).values('id', 'name', 'imdb_score', 'number_99popularity', 'genre', 'director')
            return HttpResponse(http_response_smart(list(movie_data), "Movie Data", "success"), status=200)
        else:
            return HttpResponse(http_response_smart({}, "Parameter mismatch", "fail"), status=400)
    except Exception as e:
        print(str(e))
        return HttpResponse(http_response_smart({}, "Error: " + str(e), "fail"), status = 403)

@csrf_exempt
@api_login_required
def search_movie_by_imdb_rating(request):
    try:
        min_score = request.POST.get('score')
        if min_score:
            movie_data = MovieStore.objects.filter(imdb_score__gte=min_score).values('id', 'name', 'imdb_score', 'number_99popularity', 'genre', 'director')
            return HttpResponse(http_response_smart(list(movie_data), "Movie Data", "success"), status=200)
        else:
            return HttpResponse(http_response_smart({}, "Parameter mismatch", "fail"), status=400) 
    except Exception as e:
        print(str(e))
        return HttpResponse(http_response_smart({}, "Error: " + str(e), "fail"), status = 403)

@csrf_exempt
@api_login_required
def search_movie_by_popularity(request):
    try:
        min_popularity = request.POST.get('popularity')
        if min_popularity:
            movie_data = MovieStore.objects.filter(number_99popularity__gte=min_popularity).values('id', 'name', 'imdb_score', 'number_99popularity', 'genre', 'director')
            return HttpResponse(http_response_smart(list(movie_data), "Movie Data", "success"), status=200)
        else:
            return HttpResponse(http_response_smart({}, "Parameter mismatch", "fail"), status=400)
    except Exception as e:
        print(str(e))
        return HttpResponse(http_response_smart({}, "Error: " + str(e), "fail"), status = 403)

@csrf_exempt
@api_login_required
def search_movie_by_director(request):
    try:
        dir_name_regex = request.POST.get('director_regex')
        if dir_name_regex:
            movie_data = MovieStore.objects.filter(director__icontains=dir_name_regex).values('id', 'name', 'imdb_score', 'number_99popularity', 'genre', 'director')
            return HttpResponse(http_response_smart(list(movie_data), "Movie Data", "success"), status=200)
        else:
            return HttpResponse(http_response_smart({}, "Parameter mismatch", "fail"), status=400)
    except Exception as e:
        print(str(e))
        return HttpResponse(http_response_smart({}, "Error: " + str(e), "fail"), status = 403)