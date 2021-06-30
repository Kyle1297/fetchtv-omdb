from django.db import models
from django.urls import reverse
from .validators import year_range_validator

class Video(models.Model):

    class VideoType(models.TextChoices):
        MOVIE = "MOVIE", "Movie"
        SERIES = "SERIES", "Series"
        EPISODE = "EPISODE", "Episode"

    imdb_id = models.CharField("IMDb ID", primary_key=True, max_length=100)
    title = models.CharField("Title", max_length=255, db_index=True)
    type = models.CharField("Type", max_length=20, choices=VideoType.choices, db_index=True)
    year = models.CharField("Year", max_length=9, validators=[year_range_validator]) # ideally, would use PostgreSQL IntegerRangeField

    def __str__(self) -> str:
        return f"'{self.title}', {self.year} - {self.type}"

    def save(self, *args, **kwargs) -> None:
        """
        Validate year field on save.
        """
        year_range_validator(self.year)
        return super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse('omdb_form')

    def generate_imdb_link(self) -> str:
        IMDB_GENERIC_LINK = "https://www.imdb.com/title"
        return f"{IMDB_GENERIC_LINK}/{self.imdb_id}"