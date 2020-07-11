from django.conf.urls import url
from imdb_action import views

urlpatterns = [
    url(r'^get_all_movies/', views.get_all_movies),
    url(r'^search_movie/', views.search_movie),
    url(r'^import_movie_data_from_json/', views.import_movie_data_from_json),
    url(r'^search_movie_by_name/', views.search_movie_by_name),
    url(r'^search_movie_by_imdb_rating/', views.search_movie_by_imdb_rating),
    url(r'^search_movie_by_director/', views.search_movie_by_director),
    url(r'^search_movie_by_popularity/', views.search_movie_by_popularity)
]
