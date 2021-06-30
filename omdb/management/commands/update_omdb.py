from ...utils import get_response
import requests
from ...models import Video
from django.conf import settings
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Updates local storage of OMDb records.'

    def handle(self, *args, **kwargs):
        """
        Update stored videos, one at a time.

        Note, until OMDB updates their API and allows a list of
        ids to be searched at once, this process will be quite
        inefficient and slow.

        For now, please use infrequently and conservatively.
        """

        # fetch list of videos from db and iterate through each
        video_ids = Video.objects.values_list('pk', flat=True)
        for index, video_id in enumerate(video_ids):
            # signal progress
            if index % 10 == 0:
                self.stdout.write(f"{index}/{len(video_ids)}")

            # update video record
            params = {
                "apikey": settings.OMDB_API_KEY,
                "i": video_id,
            }
            self.update_single_omdb(params)
    
        self.stdout.write("Success!")

    def update_single_omdb(self, params: dict = {}) -> list:
        """
        Fetches single result from omdb records and updates the
        corresponding result in local database.
        """
        try: 
            # update video in db
            data = get_response(settings.OMDB_API, params)
            if data.get('Response') == "True":
                Video.objects.filter(pk=data.get('imdbID')).update(
                    title=data.get('Title'),
                    type=data.get('Type').upper(),
                    year=data.get('Year'),
                )

            # handle errors
            else:
                error = data.get('Error', 'Unknown error. Try again later.')
                self.stdout.write(error)

        # handle exit messages
        except requests.exceptions.RequestException as error:
            self.stdout.write(error)