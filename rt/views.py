import helper
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rt.models import Movie_Suggestion, MovieDB, ActorDB, MovieStarred, Actor_Suggestion

def index(request):
	state = 'Not logged in.'
	un = ''
	uid = 0
	if 'username' in request.session:
		un = str(request.session['username'])
		uid = request.session['uid']
		state = 'Hello ' + un + '.'
	#Login post
	if request.POST:
			username = request.POST.get('username')
			password = request.POST.get('password')
			
			user = authenticate(username=username, password=password)
			if user is not None:
				request.session['username'] = user.username
				request.session['uid'] = user.id
				state = 'Hello ' + str(request.session['username']) + '.'
				return render(request, 'index.html', {'state':state, 'uid':request.session['uid']})
			else:
				state = 'Username/password do not match.'
				return render(request, 'login.html', {'state':state, 'uid':0})
	return render(request, 'index.html', {'state':state, 'uid':uid})

def error(request):
	uid = 0
	if 'username' in request.session:
		un = str(request.session['username'])
		uid = request.session['uid']
	return render(request, 'error.html', {'uid':uid})

def perm_denied(request):
	uid = 0
	if 'username' in request.session:
		un = str(request.session['username'])
		uid = request.session['uid']
	return render(request, 'perm_denied.html', {'uid':uid})
	
def login(request):
	state = ''
	uid = 0
	if 'username' in request.session:
		un = str(request.session['username'])
		uid = request.session['uid']
	return render(request, 'login.html', {'state':state, 'uid':uid})	

def logout(request):
	uid = 0
	if 'username' in request.session:
		un = str(request.session['username'])
		uid = request.session['uid']
	try:
		del request.session['username']
		del request.session['uid']
   	except KeyError:
		state = 'You are currently not logged in.'
		return render(request, 'error.html', {'state':state})
	return render(request, 'logout.html', {'uid':uid})

def register(request):
	state = ''
	uid = 0
	if 'username' in request.session:
		state = 'Cannot register when logged in. Please log off first.'
		return render(request, 'perm_denied.html', {'state':state})
	else:
		return render(request, 'register.html', {'state':state})

def register_confirm(request):
	uid = 0
	if 'username' in request.session:
		un = str(request.session['username'])
		uid = request.session['uid']
	state = 'Registration failed.'
	if request.POST:
		fname = request.POST.get('firstname')
		fname = request.POST['firstname']
		lname = request.POST.get('lastname')
		email = request.POST.get('email')
		username = request.POST.get('username')
		password = request.POST.get('password')
		cpassword = request.POST.get('confirmPassword')
		if str(fname) == '' or str(lname) == '' or str(email) == '' or str(username) == '' or str(password) == '' or str(cpassword) == '':
			state = "A field is incomplete."
			return render(request, 'error.html', {'state':state})
		elif helper.user_present(username):
			state = 'The username ' + username + ' is already taken. Please choose another one.'
			return render(request, 'register.html', {'state':state, 'uid':uid})
		else:
			user = User.objects.create_user(username, email, password)
			user.first_name = fname
			user.last_name = lname
			user.save()
			state = fname + ' ' + lname
			return render(request, 'register_confirm.html', {'state':state, 'uid':uid})
	return render(request, 'error.html', {'state':state, 'uid':uid})

def movie_main(request):
	state = ''
	perm = ''
	uid = 0
	movies = MovieDB.objects.all()
	titles = helper.sort_title(movies)
	ids = helper.sort_id(movies, titles)
	if 'username' in request.session:
		uid = request.session['uid']
		user = User.objects.get(username=request.session['username'])
		if user.is_staff:
			perm = 'a'
		else:
			perm = 'u'
	return render(request, 'movie_main.html', {'state':state, 'perm':perm, 'ids':ids, 'uid':uid})

def movie_suggest(request):
	state = ''
	uid = 0
	if 'username' in request.session:
		un = str(request.session['username'])
		uid = request.session['uid']
	if not 'username' in request.session:
                state = "You do not have the permissions to suggest a movie."
                return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	return render(request, 'movie_suggest.html', {'state':state, 'uid':uid})

def movie_suggest_confirm(request):
	st1 = st2 = st3 = st4 = st5 = st6 = ''
	uid = 0
	if not 'username' in request.session:
		state = "You do not have the permissions to suggest a movie."
		return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	else:
		uid = request.session['uid']
	if request.POST:
		ti = request.POST.get('title')
		if len(ti) > 0:
			ti = ti[0].capitalize() + ti[1:]
		ye = request.POST.get('year')
		di = request.POST.get('director')
		pr = request.POST.get('producer')
		ac = request.POST.get('actor')
		sy = request.POST.get('synopsis')
		movie = Movie_Suggestion(title=ti, year=ye, director=di, producer=pr, actors=ac, synopsis=sy, rating=0)
		st1 = str(movie.title)
		st2 = str(movie.year)
		st3 = str(movie.director)
		st4 = str(movie.producer)
		st5 = str(movie.actors)
		st6 = str(movie.synopsis)
		if not ti == '' and not ye == '' and not di == '' and not pr == '' and not ac == '' and not sy == '':
			movie.save()
			return render(request, 'movie_suggest_confirm.html', {'title':st1, 'year':st2, 'director':st3, 'producer':st4, 'actors':st5, 'synopsis':st6, 'uid':uid})
		else:
			state = 'All fields need to be completed.'
			return render(request, 'error.html', {'state':state})

def movie_add(request):
	uid = 0
	if 'username' in request.session:
		uid = request.session['uid']
		user = User.objects.get(username=request.session['username'])
		if not user.is_staff:
			state = "You do not have the permissions to add a movie."
			return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	else:
		state = "You are not logged in."
		return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	movies = Movie_Suggestion.objects.all()
	li = []
	for i in movies:
		li.append(i.title)
	return render(request, 'movie_add.html', {'movies':li, 'uid':uid})

def movie_add_confirm(request, i):
	uid = 0
	if 'username' in request.session:
		uid = request.session['uid']
		user = User.objects.get(username=request.session['username'])
		if not user.is_staff:
			state = "You do not have the permissions to add a movie."
			return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	else:
		state = "You are not logged in."
		return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	state = ''
	st1 = st2 = st3 = st4 = st5 = st6 = ''
	movies = Movie_Suggestion.objects.all()
	if int(i) > len(movies):
		state = 'The movie does not exist in the suggestion database anymore.'
	else:
		movie = movies[int(i)-1]
		st1 = str(movie.title)
		st2 = str(movie.year)
		st3 = str(movie.director)
		st4 = str(movie.producer)
		st5 = str(movie.actors)
		st6 = str(movie.synopsis)
	return render(request, 'movie_add_confirm.html', {'state':state, 'title':st1, 'year':st2, 'director':st3, 'producer':st4, 'actors':st5, 'synopsis':st6, 'num':i, 'uid':uid})

def movie_add_end(request, i):
	uid = 0
	if 'username' in request.session:
		uid = request.session['uid']
		user = User.objects.get(username=request.session['username'])
		if not user.is_staff:
			state = "You do not have the permissions to add a movie."
			return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	else:
		state = "You are not logged in."
		return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	state = ''
	st1 = ''
	if request.POST:
		num = int(i)
		li = Movie_Suggestion.objects.all()
		confirm = request.POST.get('accept')
		movie = li[num-1]
		st1 = str(movie.title)
		st2 = str(movie.year)
		st3 = str(movie.director)
		st4 = str(movie.producer)
		st5 = str(movie.actors)
		st6 = str(movie.synopsis)
		if confirm == 'y' or confirm == 'yes':
			#Checks if the movie is already in the database
			try:
				MovieDB.objects.get(title=st1)
				state = "The movie is already in the database. The suggestion will be deleted. Please edit the current movie."
			except MovieDB.DoesNotExist:
				ac = st5.split(', ')
				#Checks the relational property of Movie-Actor. If the actor is not present, add the actor
				for i in ac:
					try:
						ActorDB.objects.get(name=i)
					except ActorDB.DoesNotExist:
						if len(i) > 0:
							i = i[0].capitalize() + i[1:]
						newActor = ActorDB(name=i, rating=0)
						newActor.save()
				newMovie = MovieDB(title=st1, year=st2, director=st3, producer=st4, synopsis=st6, rating=0)
				newMovie.save()
				
				#Adds to the Movie-Actor relational table
				for i in ac:
					try:
						addActor = ActorDB.objects.get(name=i)
						try:
							MovieStarred.objects.get(mID=newMovie, aID=addActor)
						except MovieStarred.DoesNotExist:
							newMARelation = MovieStarred(mID=newMovie, aID=addActor)
							newMARelation.save()
					except ActorDB.DoesNotExist:
						continue
				
				state = "The movie has been successfully added to the database."
			movie.delete()
		elif confirm == 'n' or confirm == 'no':
			movie.delete()
			state = "The addition of this movie has been refused."
		else:
			state = "No changes have been made. Please answer correctly 'yes' or 'no' in the previous page."
	return render(request, 'movie_add_end.html', {'state':state, 'title':st1, 'uid':uid})

def movie_info(request, i):
	state = ''
	st1 = st2 = st3 = st4 = st5 = st6 = ''
	perm = ''
	uid = 0
	actorList = []
	aIDList = []
	aList = []
	if 'username' in request.session:
		uid = request.session['uid']
		user = User.objects.get(username=request.session['username'])
		if user.is_staff:
			perm = 'a'
		else:
			perm = 'u'
	try:
		movie = MovieDB.objects.get(id=i)
		st1 = movie.title
		st2 = movie.year
		st3 = movie.director
		st4 = movie.producer
		st6 = movie.synopsis
		
		try:
			moviesStarred = MovieStarred.objects.filter(mID=movie)
			actors = []
			for l in moviesStarred:
				actors.append(l.aID)
			for i in actors:
				actorList.append(i.name)
			for j in actorList:
				try:
					aid = ActorDB.objects.get(name=j)
					aIDList.append(aid.id)
				except ActorDB.DoesNotExist:
					continue
			for i in range(len(actors)):
				aList.append((str(actorList[i]), str(aIDList[i])))
		except MovieStarred.DoesNotExist:
			state = "Possible problem with the relational database."
	except MovieDB.DoesNotExist:
		state = "This movie does not exist in our database."
	return render(request, 'movie_info.html', {'state':state, 'title':st1, 'year':st2, 'director':st3, 'producer':st4, 'actors':aList, 'synopsis':st6, 'perm':perm, 'num':i, 'uid':uid})

def movie_delete(request, i):
	uid = 0
	if 'username' in request.session:
		uid = request.session['uid']
		user = User.objects.get(username=request.session['username'])
		if not user.is_staff:
			state = "You do not have the permissions to delete a movie."
			return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	else:
		state = "You are not logged in."
		return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	state = ''
	st1 = ''
	try:
		movie = MovieDB.objects.get(id=i)
		st1 = movie.title
	except MovieDB.DoesNotExist:
		state = "This movie does not exist."
		return render(request, 'error.html', {'state':state, 'uid':uid})
	return render(request, 'movie_delete.html', {'state':state, 'title':st1, 'num':i, 'uid':uid})

def movie_delete_confirm(request, i):
	uid = 0
	if 'username' in request.session:
		uid = request.session['uid']
		user = User.objects.get(username=request.session['username'])
		if not user.is_staff:
			state = "You do not have the permissions to add a movie."
			return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
        else:
                state = "You are not logged in."
	state = ''
	if request.POST:
                confirm = request.POST.get('accept')
		if confirm == 'y' or confirm == 'yes':
			#Removes from the MovieDB and relational database
			try:
				movie = MovieDB.objects.get(id=i)
				
				try:
					marelation = MovieStarred.objects.get(mID=movie)
					for i in marelation:
						i.delete()
				except MovieStarred.DoesNotExist:
					state = "Possible problem with the relational database."
				movie.delete()
				state = "The movie has been successfully deleted from the database."
			except MovieDB.DoesNotExist:
				state = "The movie doesn't exist in the database."
		elif confirm == 'n' or confirm == 'no':
			state = "The movie deletion has been refused. No changes have been made."
		else:
			state = "No changes have been made. Please answer correctly in the previous page with 'yes' or 'no'."
	return render(request, 'movie_delete_confirm.html', {'state':state, 'uid':uid})
	
def actor_info(request, i):
	state = ''
	st1 = st2 = st3 = ''
	perm = ''
	uid = 0
	if 'username' in request.session:
		uid = request.session['uid']
		user = User.objects.get(username=request.session['username'])
		if user.is_staff:
			perm = 'a'
		else:
			perm = 'u'
	try:
		movie = ActorDB.objects.get(id=i)
		st1 = movie.name
		st2 = movie.placeofbirth
		st3 = movie.dateofbirth
	except ActorDB.DoesNotExist:
		state = "This actor does not exist in our database."
	return render(request, 'actor_info.html', {'state':state, 'name':st1, 'placeofbirth':st2, 'dateofbirth':st3, 'perm':perm, 'num':i, 'uid':uid})
	
def actor_main(request):
	state = ''
	perm = ''
	uid = 0
	actors = ActorDB.objects.all()
	names = helper.sort_name(actors)
	ids = helper.sort_actor_id(actors, names)
	if 'username' in request.session:
		uid = request.session['uid']
		user = User.objects.get(username=request.session['username'])
		if user.is_staff:
			perm = 'a'
		else:
			perm = 'u'
	return render(request, 'actor_main.html', {'state':state, 'perm':perm, 'ids':ids, 'uid':uid})
	
def actor_suggest(request):
	state = ''
	uid = 0
	if 'username' in request.session:
		un = str(request.session['username'])
		uid = request.session['uid']
	if not 'username' in request.session:
                state = "You do not have the permissions to suggest an actor."
                return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	return render(request, 'actor_suggest.html', {'state':state, 'uid':uid})
	
def actor_suggest_confirm(request):
	st1 = st2 = st3 = st4 = ''
	uid = 0
	if not 'username' in request.session:
		state = "You do not have the permissions to suggest a movie."
		return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	else:
		uid = request.session['uid']
	if request.POST:
		na = request.POST.get('name')
		if len(na) > 0:
			na = na[0].capitalize() + na[1:]
		pl = request.POST.get('placeofbirth')
		da = request.POST.get('dateofbirth')
		mo = request.POST.get('movies')
		actor = Actor_Suggestion(name=na, placeofbirth=pl, dateofbirth=da, movies=mo, rating=0)
		st1 = str(actor.name)
		st2 = str(actor.placeofbirth)
		st3 = str(actor.dateofbirth)
		st4 = str(actor.movies)
		if not na == '' and not pl == '' and not da == '' and not mo == '':
			actor.save()
			return render(request, 'actor_suggest_confirm.html', {'name':st1, 'placeofbirth':st2, 'dateofbirth':st3, 'movies':st4, 'uid':uid})
		else:
			state = 'All fields need to be completed.'
			return render(request, 'error.html', {'state':state})
