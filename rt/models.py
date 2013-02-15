from django.db import models

class Movie_Suggestion(models.Model):
	title = models.CharField('Title', primary_key=True, max_length=50)
	year = models.IntegerField('Year')
	director = models.CharField('Director', max_length=50)
	producer = models.CharField('Producer', max_length=50)
	actors = models.CharField('Actors', max_length=200)
	synopsis = models.CharField('Synopsis', max_length=5000)
	rating = models.IntegerField('Rating')

	def __unicode__(self):
		return self.title

class MovieDB(models.Model):
	title = models.CharField('Title', max_length=50)
	year = models.IntegerField('Year')
	director = models.CharField('Director', max_length=50)
	producer = models.CharField('Producer', max_length=50)
	synopsis = models.CharField('Synopsis', max_length=5000)
	rating = models.IntegerField('Rating')

	def __unicode__(self):
		return self.title
		
class ActorDB(models.Model):
	name = models.CharField('Name', max_length=100)
	placeofbirth = models.CharField('Place of birth', max_length=100)
	dateofbirth = models.CharField('Date of birth', max_length=10)
	rating = models.IntegerField('Rating')
	
	def __unicode__(self):
		return self.name
		
class MovieStarred(models.Model):
	mID = models.ForeignKey('MovieDB')
	aID = models.ForeignKey('ActorDB')
	
	def __unicode__(self):
		return self.mID
