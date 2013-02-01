from django.db import models

class Movie(models.Model):
        title = models.CharField('Title', primary_key=True, max_length=50)
        year = models.IntegerField('Year')
        director = models.CharField('Director', max_length=50)
        actors = models.CharField('Actors', max_length=200)
        synopsis = models.CharField('Synopsis', max_length=5000)

        def __unicode__(self):
                return self.title
