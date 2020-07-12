from django.shortcuts import render
from django.http import HttpResponse
from imdb_action.decorators import http_response_smart, admin_required
from django.views.decorators.csrf import csrf_exempt
from imdb_action.models import MovieStore
import json

# Create your views here.
@csrf_exempt
@admin_required
def add_new_movie(request):
    try:
        movie_name = request.POST.get('movie_name')
        director = request.POST.get('director')
        genre = request.POST.get('genre')
        popularity = request.POST.get('popularity')
        score = request.POST.get('imdb_score')
        if not MovieStore.objects.filter(name=movie_name.strip()).exists():
            movie_obj = MovieStore(name=movie_name, imdb_score=score, genre=genre, number_99popularity=popularity, director=director)
            movie_obj.save()
            return HttpResponse(http_response_smart({}, "Movie Data added successfully", "success"),status = 200)
        else:
            return HttpResponse(http_response_smart({}, "Movie: " + movie_name + " already exists!", "success"),status = 200)
    except Exception as e:
        print(str(e))
        return HttpResponse(http_response_smart({}, "Error: " + str(e), "fail"), status = 403)


@csrf_exempt
@admin_required
def delete_movie_by_id(request):
    try:
        movie_id = request.POST.get('movie_id')
        if movie_id:
            movie_obj = MovieStore.objects.filter(id=movie_id)
            movie_obj.delete()
            return HttpResponse(http_response_smart({}, "Movie id: " + movie_id + " deleted", "success"),status = 200)
        else:
            return HttpResponse(http_response_smart({}, "Parameter mismatch", "fail"), status=400)
    except Exception as e:
        print(str(e))
        return HttpResponse(http_response_smart({}, "Error: " + str(e), "fail"), status = 403)

# This can be optional since the API call from frontend 
# can send the movie ID every time and we can delete by ID, 
# still added as optional
@csrf_exempt
@admin_required
def delete_movie_by_name(request):
    try:
        movie_name = request.POST.get('movie_name')
        if movie_name:
            movie_obj = MovieStore.objects.filter(name__iexact=movie_name)
            movie_obj.delete()
        else:
            return HttpResponse(http_response_smart({}, "Parameter mismatch", "fail"), status=400)
        return HttpResponse(http_response_smart({}, "Movie: " + movie_name + " deleted", "success"),status = 200)
    except Exception as e:
        print(str(e))
        return HttpResponse(http_response_smart({}, "Error: " + str(e), "fail"), status = 403)

@csrf_exempt
@admin_required
def edit_movie_details(request):
    try:
        movie_id = request.POST.get('movie_id')
        param_name = request.POST.get('edit_param')
        new_value = request.POST.get('new_value')
        old_value = ""
        if not movie_id or not param_name or not new_value:
            return HttpResponse(http_response_smart({}, "Parameter mismatch", "fail"), status=400)
        movie_objects = MovieStore.objects.filter(id=movie_id)
        if movie_objects:
            movie_obj = movie_objects[0]
            if param_name == "name":
                old_value = movie_obj.name
                if old_value == new_value:
                    return HttpResponse(http_response_smart({}, "New movie name matches old name", 'success'), status=200)
                movie_obj.name = new_value
            if param_name == "rating":
                old_value = movie_obj.imdb_score
                if old_value == new_value:
                    return HttpResponse(http_response_smart({}, "New rating matches old rating", 'success'), status=200)
                movie_obj.imdb_score = new_value
            if param_name == "popularity":
                old_value = movie_obj.number_99popularity
                if old_value == new_value:
                    return HttpResponse(http_response_smart({}, "New popularity matches old popularity", 'success'), status=200)
                movie_obj.number_99popularity = new_value
            # Here, I am considering the user is trying to add a genre to existing genre list. 
            # This can be replaced by removing all existing genre and creating new list as well
            if param_name == "genre":
                old_value = movie_obj.genre
                if new_value in old_value.split(','):
                    return HttpResponse(http_response_smart({}, "This Genre already exists for this movie", 'success'), status=200)
                else:
                    old_value = old_value.split(",") + [new_value]
                    movie_obj.genre = ",".join(old_value)
            if param_name == "director":
                old_value = movie_obj.director
                if old_value == new_value:
                    return HttpResponse(http_response_smart({}, "New director name matches old director name", 'success'), status=200)
                movie_obj.director = new_value
            movie_obj.save()
            return HttpResponse(http_response_smart({}, "Value Updated Successfully", 'success'), status=200)
    except Exception as e:
        print(str(e))
        return HttpResponse(http_response_smart({}, "Error: " + str(e), "fail"), status = 403)

# This function was created to load a movie JSON file, 
# which can be helpful in future case
@csrf_exempt
@admin_required
def import_movie_data_from_json(request):
    try:
        json_file = request.FILES["movie_json"]
        data = json.load(json_file)
        for row in data:
            movie_name = row["name"]
            if not MovieStore.objects.filter(name=movie_name.strip()).exists():
                movie_obj = MovieStore(name=movie_name, imdb_score=row['imdb_score'], genre=",".join(row['genre']), number_99popularity=row['99popularity'], director=row['director'])
                movie_obj.save()
        return HttpResponse(http_response_smart({}, "Data Imported successfully", "success"), status=200)
    except Exception as e:
        print(str(e))
        return HttpResponse(http_response_smart({}, "Error: " + str(e), "fail"), status=403)