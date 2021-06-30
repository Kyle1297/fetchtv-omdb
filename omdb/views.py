import urllib
from django.urls import reverse_lazy
import requests, logging
from django.views import generic
from django.db.models import Q
from .forms import OmdbForm
from .models import Video
from django.conf import settings
from .utils import get_response
from django.http.response import HttpResponse, HttpResponseRedirect


class OmdbFormView(generic.FormView):
    template_name = 'omdb_form.html'
    form_class = OmdbForm
    success_url = reverse_lazy('search_results')

    def form_valid(self, form) -> HttpResponse:
        """
        If the form is valid, redirect to the supplied URL.
        """ 
        input = form.cleaned_data
        url = self.get_success_url() + "?" + urllib.parse.urlencode(input)
        return HttpResponseRedirect(url)


class SearchResultsView(generic.ListView):
    model = Video
    template_name = 'search_results.html'
    context_object_name = "videos"
    error = ""
    
    def get_context_data(self, **kwargs):
        """
        Update data available to view template.
        """

        # display and initialize omdb form with inputted search values
        context = super(SearchResultsView, self).get_context_data(**kwargs)
        input = self.retrieve_input()
        context['form'] = OmdbForm(initial=input)

        # handle errors
        if self.error:
            if self.error == "Movie not found!" and input["type"] != Video.VideoType.MOVIE:
                context['error'] = f"{input['type'].capitalize()} not found!"   
            else:
                context['error'] = self.error

        return context
    
    def get_queryset(self):
        """
        Query results based on search.
        """

        # retrieve search values
        input = self.retrieve_input()
        query, type = input['query'], input['type']

        # ensure non-empty query or type values
        if not query or not type:
            return []

        # fetch results from local db
        object_list = Video.objects.filter((
            Q(imdb_id__icontains=query) | 
            Q(title__icontains=query)) &
            Q(type=type)
        )

        # if insufficient results, fetch data from OMDb API
        if len(object_list) < settings.MINIMUM_ENTRIES:
            params = {
                "apikey": settings.OMDB_API_KEY,
                "page": 1,
                "type": type,
                "s": query,
            }
            new_videos = self.fetch_omdb(params)
            if len(new_videos) > 0:
                object_list = new_videos

        return object_list

    def retrieve_input(self) -> dict:
        request = self.request.GET
        return {
            "query": request.get('query', ''),
            "type": request.get('type', ''),
        }

    def fetch_omdb(self, params: dict = {}) -> list:
        """
        Retrieve results from the omdb database, given a
        dictionary of query parameters.

        Returns a queryset of the results.
        """
        try: 
            # add fetched videos to db - note, cannot bulk create without generating duplicates
            data = get_response(settings.OMDB_API, params)
            if data.get('Response') == "True":
                new_videos = []
                for video in data.get('Search', []):
                    # attempt to add new video
                    try:
                        new_video = Video(
                            imdb_id=video.get('imdbID'),
                            title=video.get('Title'),
                            type=video.get('Type').upper(),
                            year=video.get('Year'),
                        )
                        new_video.save()
                        new_videos.append(new_video)
                    except Exception as error:
                        logging.error(error)
                        
                return new_videos

            # handle errors
            else:
                self.error = data.get('Error', 'Unknown error. Try again later.')
            
        except requests.exceptions.RequestException as error:
            self.error = data.get('Error', error)
            logging.error(error)

        return []