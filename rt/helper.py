from django.contrib.auth.models import User
from rt.models import Movie_Suggestion, Movie_List

def user_present(username):
	if User.objects.filter(username=username).count():
		return True	
	return False
	
#Takes in a list of Movie_List objects
#Outputs a list of sorted titles
def sort_title(movies):
	titles = []
	for i in movies:
		titles.append(str(i.title))
	titles.sort()
	return titles
	
#Takes a list of Movie_List objects and their titles as Strings
#Output a list of tuples containing the (title, id)
def sort_id(movies, titles):
	ids = []
	for i in titles:
		try:
			movie_id = Movie_List.objects.get(title=i).id
			ids.append((i, movie_id))
		except Movie_List.DoesNotExist:
			return []
	return ids
