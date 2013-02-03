from django.db import models

class Movie_Suggestion(models.Model):
        title = models.CharField('Title', primary_key=True, max_length=50)
        year = models.IntegerField('Year')
        director = models.CharField('Director', max_length=50)
	producer = models.CharField('Producer', max_length=50)
        actors = models.CharField('Actors', max_length=200)
        synopsis = models.CharField('Synopsis', max_length=5000)

        def __unicode__(self):
                return self.title

class Movie_List(models.Model):
	title = models.CharField('Title', max_length=50)
	year = models.IntegerField('Year')
	director = models.CharField('Director', max_length=50)
	producer = models.CharField('Producer', max_length=50)
	actors = models.CharField('Actors', max_length=200)
	synopsis = models.CharField('Synopsis', max_length=5000)

	def __unicode__(self):
		return self.title
