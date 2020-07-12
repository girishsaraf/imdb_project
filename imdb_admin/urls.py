from imdb_admin import views
from django.conf.urls import url

urlpatterns = [
    url(r'^add_new_movie/', views.add_new_movie),
    url(r'^delete_movie_by_id/', views.delete_movie_by_id),
    url(r'^delete_movie_by_name/', views.delete_movie_by_name),
    url(r'^edit_movie_details/', views.edit_movie_details),
    url(r'^import_movie_data_from_json/', views.import_movie_data_from_json)
]
