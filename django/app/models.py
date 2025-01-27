from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Category(models.Model):

    class CategoryTypes(models.TextChoices):
        TODO_LIST = 'todo_list', _('Todo List')
        MOVIE = 'movie', _('Movie')
        TV_SHOW = 'tv_show', _('TV Show')
        ANIME = 'anime', _('Anime')
        # BOOK = 'book', _('Book')
        # MANGA = 'manga', _('Manga')
        # MUSIC = 'music', _('Music')
        # VIDEO_GAME = 'video_game', _('Video Game')

    CATEGORY_URLS = {
        CategoryTypes.TODO_LIST: 'NOT NEEDED',
        CategoryTypes.MOVIE: 'https://api.themoviedb.org/3',
        CategoryTypes.TV_SHOW: 'https://api.themoviedb.org/3',
        CategoryTypes.ANIME: 'https://api.myanimelist.net/v2/anime',
        # CategoryTypes.BOOK: 'https://api2.isbndb.com/books/',
        # CategoryTypes.MANGA: 'manga',
        # CategoryTypes.MUSIC: 'https://musicbrainz.org/ws/2/',
        # CategoryTypes.VIDEO_GAME: 'video_game',
    }

    title = models.CharField(max_length = 25)
    type = models.CharField(max_length = 10, choices = CategoryTypes.choices)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.title
        
    def get_api_url(self):
        return self.CATEGORY_URLS[self.type]
    
    def item_count(self):
        return self.items.count()
    
class Item(models.Model):
    api_id = models.IntegerField(null = True)
    title = models.CharField(max_length = 50)
    description = models.TextField(blank = True)
    user_note = models.TextField(blank = True)
    image = models.URLField(max_length = 200, blank = True)
    user_grade = models.IntegerField(null = True)
    grade = models.FloatField(null = True)
    release_year = models.IntegerField(null = True)
    complete = models.BooleanField(default = False)
    created = models.DateTimeField(auto_now_add = True)
    category = models.ForeignKey(Category, related_name = "items", on_delete = models.CASCADE)
    additional_info = models.JSONField(null = True)

    def __str__(self):
        return self.title
