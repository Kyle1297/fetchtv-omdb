from django.urls import path

from .views import SearchResultsView, OmdbFormView

urlpatterns = [
    path('', OmdbFormView.as_view(), name='omdb_form'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
]