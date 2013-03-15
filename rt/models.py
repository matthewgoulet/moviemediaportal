from django.db import models

class Movie_Suggestion(models.Model):
	title = models.CharField('Title', primary_key=True, max_length=50)
	year = models.IntegerField('Year')
	director = models.CharField('Director', max_length=50)
	producer = models.CharField('Producer', max_length=50)
	actors = models.CharField('Actors', max_length=2000)
	synopsis = models.CharField('Synopsis', max_length=5000)

	def __unicode__(self):
		return self.title
		
class Movie_Edit(models.Model):
	title = models.CharField('Title', max_length=50)
	year = models.IntegerField('Year')
	director = models.CharField('Director', max_length=50)
	producer = models.CharField('Producer', max_length=50)
	actors = models.CharField('Actors', max_length=2000)
	synopsis = models.CharField('Synopsis', max_length=5000)

	def __unicode__(self):
		return self.title

class Actor_Edit(models.Model):
	name = models.CharField('Name', max_length=100)
	placeofbirth = models.CharField('Place of birth', max_length=100)
        dateofbirth = models.CharField('Date of birth', max_length=10)
	movies = models.CharField('Movies', max_length=500)

	def __unicode__(self):
		return self.name

class MovieDB(models.Model):
	title = models.CharField('Title', max_length=50)
	year = models.IntegerField('Year')
	director = models.CharField('Director', max_length=50)
	producer = models.CharField('Producer', max_length=50)
	synopsis = models.CharField('Synopsis', max_length=5000)

	def __unicode__(self):
		return self.title
		
class Actor_Suggestion(models.Model):
	name = models.CharField('Name', max_length=100)
	placeofbirth = models.CharField('Place of birth', max_length=100)
	dateofbirth = models.CharField('Date of birth', max_length=10)
	movies = models.CharField('Movies', max_length=5000)
	
	def __unicode__(self):
		return self.name
		
class ActorDB(models.Model):
	name = models.CharField('Name', max_length=100)
	placeofbirth = models.CharField('Place of birth', max_length=100)
	dateofbirth = models.CharField('Date of birth', max_length=10)
	
	def __unicode__(self):
		return self.name
		
class MovieStarred(models.Model):
	mID = models.ForeignKey('MovieDB')
	aID = models.ForeignKey('ActorDB')
	
	def __unicode__(self):
		return self.mID

class MovieRating(models.Model):
	username = models.CharField('Username', max_length=50)
	mID = models.ForeignKey('MovieDB')
	rating = models.IntegerField('Rating')

	def __unicode__(self):
		return self.mID

class ActorRating(models.Model):
	username = models.CharField('Username', max_length=50)
	aID = models.ForeignKey('ActorDB')
	rating = models.IntegerField('Rating')

	def __unicode__(self):
		return self.aID

class Website(models.Model):
	typ = models.CharField('Option', max_length=10)
	message = models.CharField('Message', max_length=5000)

	def __unicode__(self):
		return self.typ
