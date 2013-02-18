from django.contrib.auth.models import User
from rt.models import Movie_Suggestion, MovieDB, ActorDB

def user_present(username):
	if User.objects.filter(username=username).count():
		return True	
	return False
	
#Takes in a list of MovieDB objects
#Outputs a list of sorted titles
def sort_title(movies):
	titles = []
	for i in movies:
		titles.append(str(i.title))
	titles.sort()
	return titles
	
#Takes a list of MovieDB objects and their titles as Strings
#Output a list of tuples containing the (title, id)
def sort_id(movies, titles):
	ids = []
	for i in titles:
		try:
			movie_id = MovieDB.objects.get(title=i).id
			ids.append((i, movie_id))
		except MovieDB.DoesNotExist:
			return []
	return ids
	
def sort_name(actors):
	names = []
	for i in actors:
		names.append(str(i.name))
	names.sort()
	return names
	
def sort_actor_id(actors, names):
	ids = []
	for i in names:
		try:
			actor_id = ActorDB.objects.get(name=i).id
			ids.append((i, actor_id))
		except ActorDB.DoesNotExist:
			return []
	return ids
