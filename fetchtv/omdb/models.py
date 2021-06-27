import datetime
from django.db import models
from django.core.validators import MaxValueValidator

def max_year_validator(value):
    year = datetime.date.today().year
    return MaxValueValidator(year)(value)


class VideoType(models.TextChoices):
    MOVIE = "MOVIE", "movie"
    SERIES = "SERIES", "series"
    EPISODE = "EPISODE", "episode"


class Video(models.Model):
    imdbID = models.CharField("IMDb ID", primary_key=True, max_length=100)
    title = models.CharField("Title", max_length=255)
    type = models.CharField("Type", max_length=20, choices=VideoType.choices)
    year = models.PositiveIntegerField("Year", validators=[max_year_validator])

    def __str__(self) -> str:
        return f"'{self.title}', the {self.type}, {self.year}"

    def generate_imdb_link(self) -> str:
        IMDB_GENERIC_LINK = "https://www.imdb.com/title"
        return f"{IMDB_GENERIC_LINK}/{self.imdbID}"