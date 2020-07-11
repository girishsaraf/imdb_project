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

@csrf_exempt
@api_login_required
def search_movie_by_name(request):
    try:
        name_regex = request.POST.get('name_regex')
        if name_regex:
            movie_data = MovieStore.objects.filter(name__icontains=name_regex).values('id', 'name', 'imdb_score', 'number_99popularity', 'genre', 'director')
            return HttpResponse(http_response_smart(list(movie_data), "Movie Data", "success"))
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
            return HttpResponse(http_response_smart(list(movie_data), "Movie Data", "success"))
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
            return HttpResponse(http_response_smart(list(movie_data), "Movie Data", "success"))
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
            return HttpResponse(http_response_smart(list(movie_data), "Movie Data", "success"))
        else:
            return HttpResponse(http_response_smart({}, "Parameter mismatch", "fail"), status=400)
    except Exception as e:
        print(str(e))
        return HttpResponse(http_response_smart({}, "Error: " + str(e), "fail"), status = 403)


# This function was created to load the JSON file, 
# into the database, since MySQL workbench was unable to process it automatically
@csrf_exempt
def import_movie_data_from_json(request):
    try:
        with open("/Users/girishsaraf/Desktop/imdb.json", 'r') as f:
            data = json.load(f)
        for row in data:
            movie_obj = MovieStore(name=row['name'], imdb_score=row['imdb_score'], genre=",".join(row['genre']), number_99popularity=row['99popularity'], director=row['director'])
            movie_obj.save()
        return HttpResponse(http_response_smart({}, "Data Imported successfully", "success"))
    except Exception as e:
        print(str(e))
        return HttpResponse(http_response_smart({}, "Error: " + str(e), "fail"), status=403)