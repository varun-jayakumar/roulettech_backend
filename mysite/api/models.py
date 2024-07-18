from django.db import models

# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=100)
    ingredients = models.TextField()
    instructions = models.TextField()
    cuisine = models.CharField(max_length=100)

    def __str__(self):
        return self.title