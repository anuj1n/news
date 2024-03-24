from django.db import models
from django.utils import timezone

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=200)
    username = models.CharField(unique=True, primary_key=True, max_length=200)
    password = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.username
    

class Story(models.Model):
    unique_key = models.AutoField(primary_key=True)
    headline = models.CharField(max_length=64)
    CATEGORIES = [('pol', 'Politics'), ('art', 'ART'), ('tech', 'Technology'), ('trivia', 'Trivia')]
    category = models.CharField(choices=CATEGORIES, max_length=6)
    REGIONS = [('uk', 'UK News'), ('eu', 'European News'), ('w', 'World News')]
    region = models.CharField(choices=REGIONS, max_length=2)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateField()
    details = models.CharField(max_length=128)

    def __str__(self):
        return self.headline
