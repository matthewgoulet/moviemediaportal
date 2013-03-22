import helper
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms.widgets import RadioSelect

from rt.models import Movie_Suggestion, MovieDB, ActorDB, MovieStarred, Actor_Suggestion, Movie_Edit, Actor_Edit, MovieRating, ActorRating, Website, TVDB, TV_Suggestion, TVStarred, TVRating, MovieWatchlist, TVWatchlist

def index(request):
	state = 'Not logged in.'
	un = ''
	uid = 0
	perm = ""
	news = 'No news currently.'
	mwl = ''
	twl = ''
	mwl_ids = []
	twl_ids = []
	if 'username' in request.session:
		un = str(request.session['username'])
		uid = request.session['uid']
		state = 'Hello ' + un + '.'
		user = User.objects.get(username=request.session['username'])
                if user.is_staff:
                        perm = 'a'
                else:
                        perm = 'u'

	#Checks for news
	try:
		n = Website.objects.get(typ='news')
		news = n.message
	except Website.DoesNotExist:
		news = 'No news currently'

	#Checks for the watchlists
	try:
		moviesWL = MovieWatchlist.objects.filter(username=un)
		if len(moviesWL) == 0:
			mwl = 'No movies in your watchlist'
		mList = []
		for j in moviesWL:
			mList.append(j.mID)
		titles = helper.sort_title(mList)
		mwl_ids = helper.sort_id(moviesWL, titles)
	except MovieWatchlist.DoesNotExist:
		mwl = 'No movies in your watchlist'

	try:
		tvsWL = TVWatchlist.objects.filter(username=un)
		if len(tvsWL) == 0:
			twl = 'No TV shows in your watchlist'
		tList = []
		for j in tvsWL:
			tList.append(j.tID)
		titles2 = helper.sort_title(tList)
		twl_ids = helper.sort_tv_id(tvsWL, titles2)
	except TVWatchlist.DoesNotExist:
		twl = 'No TV shows in your watchlist'

	#Login post
	if request.POST:
			username = request.POST.get('username')
			password = request.POST.get('password')
			
			user = authenticate(username=username, password=password)
			if user is not None:
				request.session['username'] = user.username
				request.session['uid'] = user.id
				state = 'Hello ' + str(request.session['username']) + '.'

				mwl = ''
				twl = ''

				#Checks for the watchlist
				try:
					moviesWL = MovieWatchlist.objects.filter(username=username)
					if len(moviesWL) == 0:
						mwl = 'No movies in your watchlist'
					mList = []
					for j in moviesWL:
						mList.append(j.mID)
						titles = helper.sort_title(mList)
						mwl_ids = helper.sort_id(moviesWL, titles)
				except MovieWatchlist.DoesNotExist:
					mwl = 'No movies in your watchlist'

				try:
					tvsWL = TVWatchlist.objects.filter(username=username)
					if len(tvsWL) == 0:
						twl = 'No TV shows in your watchlist'
					tList = []
					for j in tvsWL:
						tList.append(j.tID)
						titles2 = helper.sort_title(tList)
						twl_ids = helper.sort_tv_id(tvsWL, titles2)
				except TVWatchlist.DoesNotExist:
					twl = 'No TV shows in your watchlist'

				user = User.objects.get(username=request.session['username'])
                		if user.is_staff:
                        		perm = 'a'
                		else:
                        		perm = 'u'
				
				return render(request, 'index.html', {'state':state, 'news':news, 'mids':mwl_ids, 'tids':twl_ids, 'mwl':mwl, 'twl':twl, 'uid':request.session['uid'], 'perm':perm})
			else:
				state = 'Username/password do not match.'
				return render(request, 'login.html', {'state':state, 'uid':0, 'news':news})
	return render(request, 'index.html', {'state':state, 'news':news, 'mids':mwl_ids, 'tids':twl_ids, 'mwl':mwl, 'twl':twl, 'uid':uid, 'perm':perm})

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
		if str(fname) == '' or str(lname) == '' or str(email) == '' or str(username) == '' or str(password) == '' or str(cpassword) == '' or not '@' in str(email):
			state = "All fields must be properly filled during registration."
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
	if len(ids) == 0:
		state = "No movies found in the database."
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
		movie = Movie_Suggestion(title=ti, year=ye, director=di, producer=pr, actors=ac, synopsis=sy)
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
			state = 'All fields need to be completed when suggesting a movie.'
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
					if len(i) > 0:
							i = i[0].capitalize() + i[1:]
					try:
						ActorDB.objects.get(name=i)
					except ActorDB.DoesNotExist:
						newActor = ActorDB(name=i)
						newActor.save()
				newMovie = MovieDB(title=st1, year=st2, director=st3, producer=st4, synopsis=st6)
				newMovie.save()
				
				#Adds to the Movie-Actor relational table
				for i in ac:
					if len(i) > 0:
						i = i[0].capitalize() + i[1:]
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
	rating = 0
	rat = 0
	watchlist = ''
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

		if request.POST:
			if not request.POST.get('rating') == None:
				rat = int(request.POST.get('rating'))
			if rat > 0 and rat < 6:
				try:
					userRating = MovieRating.objects.get(username=request.session['username'], mID=movie)
					userRating.rating = rat
					userRating.save()
				except MovieRating.DoesNotExist:
					userRating = MovieRating(username=request.session['username'], mID=movie, rating=rat)
					userRating.save()
	
		try:
			moviesStarred = MovieStarred.objects.filter(mID=movie)
			actors = []
			for l in moviesStarred:
				actors.append(l.aID)
			for k in actors:
				actorList.append(k.name)
			for j in actorList:
				try:
					aid = ActorDB.objects.get(name=j)
					aIDList.append(aid.id)
				except ActorDB.DoesNotExist:
					continue
			for m in range(len(actors)):
				aList.append((str(actorList[m]), str(aIDList[m])))
		except MovieStarred.DoesNotExist:
			state = "Possible problem with the relational database."

		try:
			movieRatings = MovieRating.objects.filter(mID=movie)
			totalRating = 0
			for j in movieRatings:
				totalRating = totalRating + j.rating
			if len(movieRatings) > 0:
				rating = float(totalRating) / float(len(movieRatings)) 
		except MovieRating.DoesNotExist:
			rating = 0	
		try:
			MovieWatchlist.objects.get(username=user, mID=movie)
			watchlist = 'Remove this movie from your watchlist'
		except MovieWatchlist.DoesNotExist:
			watchlist = 'Add this movie from your watchlist'
			
	except MovieDB.DoesNotExist:
		state = "This movie does not exist in our database."
	return render(request, 'movie_info.html', {'state':state, 'title':st1, 'year':st2, 'director':st3, 'producer':st4, 'actors':aList, 'synopsis':st6, 'rating':rating, 'watchlist':watchlist, 'perm':perm, 'num':i, 'uid':uid})

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
					marelation.delete()
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
	movieList = []
	mIDList = []
	mList = []
	tvList = []
	tIDList = []
	tList = []
	rating = 0
	rat = 0
	if 'username' in request.session:
		uid = request.session['uid']
		user = User.objects.get(username=request.session['username'])
		if user.is_staff:
			perm = 'a'
		else:
			perm = 'u'
	try:
		actor = ActorDB.objects.get(id=i)
		st1 = actor.name
		st2 = actor.placeofbirth
		st3 = actor.dateofbirth
	
		if request.POST:
                        if not request.POST.get('rating') == None:
                                rat = int(request.POST.get('rating'))
                        if rat > 0 and rat < 6:
                                try:
                                        userRating = ActorRating.objects.get(username=request.session['username'], aID=actor)
                                        userRating.rating = rat
                                        userRating.save()
                                except ActorRating.DoesNotExist:
                                        userRating = ActorRating(username=request.session['username'], aID=actor, rating=rat)
                                        userRating.save()
	
		try:
			moviesStarred = MovieStarred.objects.filter(aID=actor)
			movies = []
			for l in moviesStarred:
				movies.append(l.mID)
			for k in movies:
				movieList.append(k.title)
			for j in movieList:
				try:
					mid = MovieDB.objects.get(title=j)
					mIDList.append(mid.id)
				except MovieDB.DoesNotExist:
					continue
			for m in range(len(movies)):
				mList.append((str(movieList[m]), str(mIDList[m])))
		except MovieStarred.DoesNotExist:
			state = "Possible problem with the relational database."

		try:
                        tvsStarred = TVStarred.objects.filter(aID=actor)
                        tvs = []
                        for l in tvsStarred:
                                tvs.append(l.tID)
                        for k in tvs:
                                tvList.append(k.title)
                        for j in tvList:
                                try:
                                        tid = TVDB.objects.get(title=j)
                                        tIDList.append(tid.id)
                                except TVDB.DoesNotExist:
                                        continue
                        for m in range(len(tvs)):
                                tList.append((str(tvList[m]), str(tIDList[m])))
                except TVStarred.DoesNotExist:
                        state = "Possible problem with the relational database."
	
		try:
                        actorRatings = ActorRating.objects.filter(aID=actor)
                        totalRating = 0
                        for j in actorRatings:
                                totalRating = totalRating + j.rating
                        if len(actorRatings) > 0:
                                rating = float(float(totalRating) / float(len(actorRatings)))
                except ActorRating.DoesNotExist:
                        rating = 0
	
	except ActorDB.DoesNotExist:
		state = "This actor does not exist in our database."
	return render(request, 'actor_info.html', {'state':state, 'name':st1, 'placeofbirth':st2, 'dateofbirth':st3, 'movies':mList, 'tvs':tList, 'rating':rating, 'perm':perm, 'num':i, 'uid':uid})
	
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
	if len(ids) == 0:
		state = 'No actors have been found in the database.'
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
		actor = Actor_Suggestion(name=na, placeofbirth=pl, dateofbirth=da, movies=mo)
		st1 = str(actor.name)
		st2 = str(actor.placeofbirth)
		st3 = str(actor.dateofbirth)
		st4 = str(actor.movies)
		if not len(st3.split('-')) == 3:
			state = 'Invalid date during the creation of the actor profile. (MM-dd-YYYY)'
			return render(request, 'error.html', {'state':state})
		else:
			for i in st3.split('-'):
				try:
					int(i)
				except ValueError:
					state = 'Invalid date during the creation of the actor profile. (MM-dd-YY)'	
					return render(request, 'error.html', {'state':state})
		if int(st3.split('-')[0]) < 0 or int(st3.split('-')[1]) < 0 or int(st3.split('-')[2]) < 0 or int(st3.split('-')[0]) > 12 or int(st3.split('-')[1]) > 31:
			state = 'Invalid date during the creation of the actor profile. (MM-dd-YYYY)'
                        return render(request, 'error.html', {'state':state})
		if not na == '' and not pl == '' and not da == '' and not mo == '':
			actor.save()
			return render(request, 'actor_suggest_confirm.html', {'name':st1, 'placeofbirth':st2, 'dateofbirth':st3, 'movies':st4, 'uid':uid})
		else:
			state = 'All fields need to be completed when suggesting an actor.'
			return render(request, 'error.html', {'state':state})
			
def actor_add(request):
	uid = 0
	if 'username' in request.session:
		uid = request.session['uid']
		user = User.objects.get(username=request.session['username'])
		if not user.is_staff:
			state = "You do not have the permissions to add an actor."
			return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	else:
		state = "You are not logged in."
		return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	actors = Actor_Suggestion.objects.all()
	li = []
	for i in actors:
		li.append(i.name)
	return render(request, 'actor_add.html', {'actors':li, 'uid':uid})
	
def actor_add_confirm(request, i):
	uid = 0
	if 'username' in request.session:
		uid = request.session['uid']
		user = User.objects.get(username=request.session['username'])
		if not user.is_staff:
			state = "You do not have the permissions to add an actor."
			return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	else:
		state = "You are not logged in."
		return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	state = ''
	st1 = st2 = st3 = st4 = ''
	actors = Actor_Suggestion.objects.all()
	if int(i) > len(actors):
		state = 'The movie does not exist in the suggestion database anymore.'
	else:
		actor = actors[int(i)-1]
		st1 = str(actor.name)
		st2 = str(actor.placeofbirth)
		st3 = str(actor.dateofbirth)
		st4 = str(actor.movies)
	return render(request, 'actor_add_confirm.html', {'state':state, 'name':st1, 'placeofbirth':st2, 'dateofbirth':st3, 'movies':st4, 'num':i, 'uid':uid})
	
def actor_add_end(request, i):
	uid = 0
	if 'username' in request.session:
		uid = request.session['uid']
		user = User.objects.get(username=request.session['username'])
		if not user.is_staff:
			state = "You do not have the permissions to add an actor."
			return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	else:
		state = "You are not logged in."
		return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	state = ''
	st1 = ''
	if request.POST:
		num = int(i)
		li = Actor_Suggestion.objects.all()
		confirm = request.POST.get('accept')
		actor = li[num-1]
		st1 = str(actor.name)
		st2 = str(actor.placeofbirth)
		st3 = str(actor.dateofbirth)
		st4 = str(actor.movies)
		if confirm == 'y' or confirm == 'yes':
			#Checks if the actor is already in the database
			try:
				ActorDB.objects.get(name=st1)
				state = "The actor is already in the database. The suggestion will be deleted. Please edit the current actor."
			except ActorDB.DoesNotExist:
				mo = st4.split(', ')
				#Checks the relational property of Movie-Actor. If the actor is not present, add the movie
				for i in mo:
					if len(i) > 0:
							i = i[0].capitalize() + i[1:]
					try:
						MovieDB.objects.get(title=i)
					except MovieDB.DoesNotExist:
						newMovie = MovieDB(title=i, year=0)
						newMovie.save()
				newActor = ActorDB(name=st1, placeofbirth=st2, dateofbirth=st3)
				newActor.save()
				
				#Adds to the Movie-Actor relational table
				for i in mo:
					if len(i) > 0:
						i = i[0].capitalize() + i[1:]
					try:
						addMovie = MovieDB.objects.get(title=i)
						try:
							MovieStarred.objects.get(mID=addMovie, aID=newActor)
						except MovieStarred.DoesNotExist:
							newMARelation = MovieStarred(mID=addMovie, aID=newActor)
							newMARelation.save()
					except ActorDB.DoesNotExist:
						continue
				
				state = "The actor has been successfully added to the database."
			actor.delete()
		elif confirm == 'n' or confirm == 'no':
			actor.delete()
			state = "The addition of this actor has been refused."
		else:
			state = "No changes have been made. Please answer correctly 'yes' or 'no' in the previous page."
	return render(request, 'actor_add_end.html', {'state':state, 'name':st1, 'uid':uid})
	
def actor_delete(request, i):
	uid = 0
	if 'username' in request.session:
		uid = request.session['uid']
		user = User.objects.get(username=request.session['username'])
		if not user.is_staff:
			state = "You do not have the permissions to delete an actor."
			return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	else:
		state = "You are not logged in."
		return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	state = ''
	st1 = ''
	try:
		actor = ActorDB.objects.get(id=i)
		st1 = actor.name
	except ActorDB.DoesNotExist:
		state = "This actor does not exist."
		return render(request, 'error.html', {'state':state, 'uid':uid})
	return render(request, 'actor_delete.html', {'state':state, 'name':st1, 'num':i, 'uid':uid})

def actor_delete_confirm(request, i):
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
			#Removes from the ActorDB and relational database
			try:
				actor = ActorDB.objects.get(id=i)
				try:
					marelation = MovieStarred.objects.filter(aID=actor)
					marelation.delete()
				except MovieStarred.DoesNotExist:
					state = "Possible problem with the relational database."
				actor.delete()
				state = "The actor has been successfully deleted from the database."
			except ActorDB.DoesNotExist:
				state = "The actor doesn't exist in the database."
		elif confirm == 'n' or confirm == 'no':
			state = "The actor deletion has been refused. No changes have been made."
		else:
			state = "No changes have been made. Please answer correctly in the previous page with 'yes' or 'no'."
	return render(request, 'actor_delete_confirm.html', {'state':state, 'uid':uid})

def movie_search(request):
	state = ''
	return render(request, 'movie_search.html', {'state':state})
	
def movie_search_result(request):
	state = ''
	ids = []
	if request.POST:
		ti = request.POST.get('title')
		if len(ti) > 0:
			ti = ti[0].capitalize() + ti[1:]
		ye = request.POST.get('year')
		di = request.POST.get('director')
		pr = request.POST.get('producer')
		ac = request.POST.get('actor')
		sy = request.POST.get('synopsis')
		
		movies = MovieDB.objects.filter(title__icontains=ti).filter(year__contains=ye).filter(director__icontains=di).filter(producer__icontains=pr).filter(synopsis__icontains=sy)
		
		if ac == '':
			titles = helper.sort_title(movies)
			ids = helper.sort_id(movies, titles)
			if len(ids) == 0:
				state = "No movies have been found to match the input specifications."
			return render(request, 'movie_search_result.html', {'state':state, 'ids':ids})
		else:
			actors = ac.split(', ')
			movies_relation = []
			for i in actors:
				if len(i) > 0:
					i = i[0].capitalize() + i[1:]
				try:
					actor_id = ActorDB.objects.get(name__iexact=i).id
				except ActorDB.DoesNotExist:
					actor_id = 0
				actor_rel = MovieStarred.objects.filter(aID=actor_id)
				for i in actor_rel:
					movies_relation.append(i.mID)
			movies_relation = list(set(movies_relation))
		
		#Gets a set of movie IDs that correspond to the search	
		movies_id = set()
		movies_rel_id = set()
		for i in movies:
			movies_id.add(i.id)
		for i in movies_relation:
			movies_rel_id.add(i.id)
		movieID_list = movies_id & movies_rel_id
		
		#Gets a list of Movie objects that correspond to the search
		movie_list = []
		for i in movieID_list:
			try:
				movie = MovieDB.objects.get(id=i)
				movie_list.append(movie)
			except MovieDB.DoesNotExist:
				continue
		
		titles = helper.sort_title(movie_list)
		ids = helper.sort_id(movie_list, titles)
		if len(ids) == 0:
			state = "No movies have been found to match the input specifications."
		return render(request, 'movie_search_result.html', {'state':state, 'ids':ids})
		
def actor_search(request):
	state = ''
	return render(request, 'actor_search.html', {'state':state})
	
def actor_search_result(request):
	state = ''
	ids = []
	if request.POST:
		na = request.POST.get('name')
		if len(na) > 0:
			na = na[0].capitalize() + na[1:]
		pl = request.POST.get('placeofbirth')
		da = request.POST.get('dateofbirth')
		mo = request.POST.get('movies')
		
		actors = ActorDB.objects.filter(name__icontains=na).filter(placeofbirth__icontains=pl).filter(dateofbirth__icontains=da)
		
		#Does the search on ActorDB
		if mo == '':
			names = helper.sort_name(actors)
			ids = helper.sort_actor_id(actors, names)
			if len(ids) == 0:
				state = "No actors have been found to match the input specifications."
			return render(request, 'actor_search_result.html', {'state':state, 'ids':ids})
		else:
			movies = mo.split(', ')
			actors_relation = []
			for i in movies:
				if len(i) > 0:
					i = i[0].capitalize() + i[1:]
				try:
					movie_id = MovieDB.objects.get(title__iexact=i).id
				except MovieDB.DoesNotExist:
					movie_id = 0
				movie_rel = MovieStarred.objects.filter(mID=movie_id)
				for i in movie_rel:
					actors_relation.append(i.aID)
			actors_relation = list(set(actors_relation))
		
		#Gets a set of actor IDs that correspond to the search	
		actors_id = set()
		actors_rel_id = set()
		for i in actors:
			actors_id.add(i.id)
		for i in actors_relation:
			actors_rel_id.add(i.id)
		actorID_list = actors_id & actors_rel_id
		
		#Gets a list of Movie objects that correspond to the search
		actor_list = []
		for i in actorID_list:
			try:
				actor = ActorDB.objects.get(id=i)
				actor_list.append(actor)
			except ActorDB.DoesNotExist:
				continue
		
		names = helper.sort_name(actor_list)
		ids = helper.sort_actor_id(actor_list, names)
		if len(ids) == 0:
			state = "No actors have been found to match the input specifications."
		return render(request, 'actor_search_result.html', {'state':state, 'ids':ids})
		
def movie_edit_suggest(request, i):
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
		
		#Makes a string of all the actors
		try:
			moviesStarred = MovieStarred.objects.filter(mID=movie)
			actors = ''
			for ac in moviesStarred:
				actors = actors + str(ac.aID.name) + ', '
			if len(actors) > 2:
				actors = actors[:-2]
		except MovieStarred.DoesNotExist:
			state = "This movie doesn't have any actors associated to it."
			
	except MovieDB.DoesNotExist:
		state = "This movie does not exist in our database."
	return render(request, 'movie_edit_suggest.html', {'state':state, 'title':st1, 'year':st2, 'director':st3, 'producer':st4, 'actors':actors, 'synopsis':st6, 'perm':perm, 'num':i, 'uid':uid})
	
def movie_edit_suggest_confirm(request, i):
	st1 = st2 = st3 = st4 = st5 = st6 = ''
	uid = 0
	if not 'username' in request.session:
		state = "You do not have the permissions to suggest a movie."
		return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	else:
		uid = request.session['uid']
	if request.POST:
		ye = request.POST.get('year')
		di = request.POST.get('director')
		pr = request.POST.get('producer')
		ac = request.POST.get('actor')
		sy = request.POST.get('synopsis')
		
		try:
			oldMovie = MovieDB.objects.get(id=i)
			oldTi = str(oldMovie.title)
			oldYe = str(oldMovie.year)
			oldDi = str(oldMovie.director)
			oldPr = str(oldMovie.producer)
			oldSy = str(oldMovie.synopsis)
			
			movie = Movie_Edit(title=oldTi, year=ye, director=di, producer=pr, actors=ac, synopsis=sy)
			st2 = str(movie.year)
			st3 = str(movie.director)
			st4 = str(movie.producer)
			st5 = str(movie.actors)
			st6 = str(movie.synopsis)
			
			try:
				moviesStarred = MovieStarred.objects.filter(mID=oldMovie)
				actors = ''
				for ac in moviesStarred:
					actors = actors + str(ac.aID.name) + ', '
				if len(actors) > 2:
					actors = actors[:-2]
			except MovieStarred.DoesNotExist:
				state = "This movie doesn't have any actors associated to it."
				
			if(st2 == oldYe and st3 == oldDi and st4 == oldPr and st5 == actors and st6 == oldSy):
				state = 'No modifications has been made for this movie.'
				return render(request, 'error.html', { 'state':state})
			
		except MovieDB.DoesNotExist:
			state = 'Could not find movie in the database.'
		if not ye == '' and not di == '' and not pr == '' and not ac == '' and not sy == '':
			movie.save()
			return render(request, 'movie_edit_suggest_confirm.html', {'title':oldTi, 'year':st2, 'director':st3, 'producer':st4, 'actors':st5, 'synopsis':st6, 'oldYear':oldYe, 'oldDirector':oldDi, 'oldProducer':oldPr, 'oldSynopsis':oldSy, 'oldActors':actors, 'uid':uid})
		else:
			state = 'All fields need to be completed when editing a movie.'
			return render(request, 'error.html', {'state':state, 'num':i})
			
def movie_edit(request):
	uid = 0
        if 'username' in request.session:
                uid = request.session['uid']
                user = User.objects.get(username=request.session['username'])
                if not user.is_staff:
                        state = "You do not have the permissions to edit a movie."
                        return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
        else:
                state = "You are not logged in."
                return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
        movies = Movie_Edit.objects.all()
        li = []
        for i in movies:
                li.append(i.title)
        return render(request, 'movie_edit.html', {'movies':li, 'uid':uid})

def movie_edit_confirm(request, i):
        uid = 0
        if 'username' in request.session:
                uid = request.session['uid']
                user = User.objects.get(username=request.session['username'])
                if not user.is_staff:
                        state = "You do not have the permissions to edit a movie."
                        return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
        else:
                state = "You are not logged in."
                return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
        state = ''
        st1 = st2 = st3 = st4 = st5 = st6 = ''
        movies = Movie_Edit.objects.all()
        if int(i) > len(movies):
                state = 'The movie does not exist in the edit database anymore.'
        else:
                movie = movies[int(i)-1]
                st1 = str(movie.title)
                st2 = str(movie.year)
                st3 = str(movie.director)
                st4 = str(movie.producer)
                st5 = str(movie.actors)
                st6 = str(movie.synopsis)
        return render(request, 'movie_edit_confirm.html', {'state':state, 'title':st1, 'year':st2, 'director':st3, 'producer':st4, 'actors':st5, 'synopsis':st6, 'num':i, 'uid':uid})

def movie_edit_end(request, i):
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
		li = Movie_Edit.objects.all()
		confirm = request.POST.get('accept')
		movie = li[num-1]
		st2 = request.POST.get('year')
                st3 = request.POST.get('director')
                st4 = request.POST.get('producer')
                st5 = request.POST.get('actor')
                st6 = request.POST.get('synopsis')

		if confirm == 'y' or confirm == 'yes':
			#Checks if the movie is already in the database
			try:
				editMovie = MovieDB.objects.get(id=i)
		
				ac = st5.split(', ')
				#Checks the relational property of Movie-Actor. If the actor is not present, add the actor
				for i in ac:
					if len(i) > 0:
							i = i[0].capitalize() + i[1:]
					try:
						ActorDB.objects.get(name=i)
					except ActorDB.DoesNotExist:
						newActor = ActorDB(name=i)
						newActor.save()

				#Deletes old actors in MovieStarred:
				oldActors = MovieStarred.objects.filter(mID=editMovie)
				for j in oldActors:
					j.delete()

				#Edits the movie information in MovieDB
				editMovie.year = st2
				editMovie.director = st3
				editMovie.producer = st4
				editMovie.synopsis = st6
				editMovie.save()
	
				#Adds to the Movie-Actor relational table
				for i in ac:
					if len(i) > 0:
						i = i[0].capitalize() + i[1:]
					try:
						addActor = ActorDB.objects.get(name=i)
						try:
							MovieStarred.objects.get(mID=editMovie, aID=addActor)
						except MovieStarred.DoesNotExist:
							newMARelation = MovieStarred(mID=editMovie, aID=addActor)
							newMARelation.save()
					except ActorDB.DoesNotExist:
						continue
				
				state = "The movie has been successfully edited in the database."
			except MovieDB.DoesNotExist:
				state = "The movie isn't in the database. The edit suggestion will be deleted."
			movie.delete()
		elif confirm == 'n' or confirm == 'no':
			movie.delete()
			state = "The edit of this movie has been refused."
		else:
			state = "No changes have been made. Please answer correctly 'yes' or 'no' in the previous page."
	return render(request, 'movie_add_end.html', {'state':state, 'title':st1, 'uid':uid})

def navigation_search(request):
	state = ''
	typ = ''
	if request.POST:
		search = str(request.POST.get('search'))
		typ = str(request.POST.get('type'))

		if typ == 'movies':
			movies = MovieDB.objects.filter(title__icontains=search)
			titles = helper.sort_title(movies)
                        ids = helper.sort_id(movies, titles)
                        if len(ids) == 0:
                                state = "No movies have been found to match the input specifications."
                        return render(request, 'navigation_search.html', {'state':state, 'ids':ids, 'typ':typ})
		elif typ == 'actors':
			actors = ActorDB.objects.filter(name__icontains=search)
			names = helper.sort_name(actors)
                        ids = helper.sort_actor_id(actors, names)
                        if len(ids) == 0:
                                state = "No actors have been found to match the input specifications."
                        return render(request, 'navigation_search.html', {'state':state, 'ids':ids, 'typ':typ})
	return render(request, 'navigation_search.html', {'state':state, 'ids':ids, 'typ':typ})

def actor_edit_suggest(request, i):
        state = ''
        st1 = st2 = st3 = ''
        perm = ''
        uid = 0
        movieList = []
        mIDList = []
        mList = []
        if 'username' in request.session:
                uid = request.session['uid']
                user = User.objects.get(username=request.session['username'])
                if user.is_staff:
                        perm = 'a'
                else:
                        perm = 'u'
        try:
                actor = ActorDB.objects.get(id=i)
                st1 = actor.name
                st2 = actor.placeofbirth
                st3 = actor.dateofbirth

                #Makes a string of all the movies
                try:
                        moviesStarred = MovieStarred.objects.filter(aID=actor)
                        movies = ''
                        for mo in moviesStarred:
                                movies = movies + str(mo.mID.title) + ', '
                        if len(movies) > 2:
                                movies = movies[:-2]
                except MovieStarred.DoesNotExist:
                        state = "This actor doesn't have any actors associated to it."
        except MovieDB.DoesNotExist:
                state = "This actor does not exist in our database."
        return render(request, 'actor_edit_suggest.html', {'state':state, 'name':st1, 'placeofbirth':st2, 'dateofbirth':st3, 'movies':movies, 'perm':perm, 'num':i, 'uid':uid})

def actor_edit_suggest_confirm(request, i):
        st1 = st2 = st3 = st4 = ''
        uid = 0
        if not 'username' in request.session:
                state = "You do not have the permissions to suggest a movie."
                return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
        else:
                uid = request.session['uid']
        if request.POST:
                pl = request.POST.get('placeofbirth')
                da = request.POST.get('dateofbirth')
		mov = request.POST.get('movies')

                try:
                        oldActor = ActorDB.objects.get(id=i)
			oldNa = str(oldActor.name)
                        oldPl = str(oldActor.placeofbirth)
                        oldDa = str(oldActor.dateofbirth)

                        actor = Actor_Edit(name=oldNa, placeofbirth=pl, dateofbirth=da, movies=mov)
                        st2 = str(actor.placeofbirth)
                        st3 = str(actor.dateofbirth)
			st4 = str(actor.movies)

                        try:
                                moviesStarred = MovieStarred.objects.filter(aID=oldActor)
                                movies = ''
                                for mo in moviesStarred:
                                        movies = movies + str(mo.mID.title) + ', '
                                if len(movies) > 2:
                                        movies = movies[:-2]
                        except MovieStarred.DoesNotExist:
                                state = "This actor doesn't have any movies associated to it."

                        if(st2 == oldPl and st3 == oldDa and st4 == movies):
                                state = 'No modifications has been made for this actor.'
                                return render(request, 'error.html', { 'state':state})

                except ActorDB.DoesNotExist:
                        state = 'Could not find the actor in the database.'
		if not pl == '' and not da == '' and not mov == '':
                        actor.save()
                        return render(request, 'actor_edit_suggest_confirm.html', {'name':oldNa, 'placeofbirth':st2, 'dateofbirth':st3, 'movies':mov, 'oldPlaceofbirth':oldPl, 'oldDateofbirth':oldDa, 'oldMovies':movies, 'uid':uid})
                else:
                        state = 'All fields need to be completed when editing an actor.'
                        return render(request, 'error.html', {'state':state, 'num':i})

def actor_edit(request):
        uid = 0
        if 'username' in request.session:
                uid = request.session['uid']
                user = User.objects.get(username=request.session['username'])
                if not user.is_staff:
                        state = "You do not have the permissions to edit an actor."
                        return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
        else:
                state = "You are not logged in."
                return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
        actors = Actor_Edit.objects.all()
        li = []
        for i in actors:
                li.append(i.name)
        return render(request, 'actor_edit.html', {'actors':li, 'uid':uid})

def actor_edit_confirm(request, i):
        uid = 0
        if 'username' in request.session:
                uid = request.session['uid']
                user = User.objects.get(username=request.session['username'])
                if not user.is_staff:
                        state = "You do not have the permissions to edit an actor."
                        return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
        else:
                state = "You are not logged in."
                return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
        state = ''
        st1 = st2 = st3 = st4 = st5 = st6 = ''
        actors = Actor_Edit.objects.all()
        if int(i) > len(actors):
                state = 'The actor does not exist in the edit database anymore.'
        else:
                actor = actors[int(i)-1]
                st1 = str(actor.name)
                st2 = str(actor.placeofbirth)
                st3 = str(actor.dateofbirth)
                st4 = str(actor.movies)
        return render(request, 'actor_edit_confirm.html', {'state':state, 'name':st1, 'placeofbirth':st2, 'dateofbirth':st3, 'movies':st4, 'num':i, 'uid':uid})

def actor_edit_end(request, i):
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
                li = Actor_Edit.objects.all()
                confirm = request.POST.get('accept')
                actor = li[num-1]
                st2 = request.POST.get('placeofbirth')
                st3 = request.POST.get('dateofbirth')
                st4 = request.POST.get('movies')

                if confirm == 'y' or confirm == 'yes':
                        #Checks if the actor is already in the database
                        try:
                                editActor = ActorDB.objects.get(id=i)

                                mo = st4.split(', ')
                                #Checks the relational property of Movie-Actor. If the movie is not present, add the actor
                                for i in mo:
                                        if len(i) > 0:
                                                        i = i[0].capitalize() + i[1:]
                                        try:
                                                MovieDB.objects.get(title=i)
                                        except MovieDB.DoesNotExist:
                                                newMovie = MovieDB(title=i)
                                                newMovie.save()

                                #Deletes old movies in MovieStarred:
				oldMovies = MovieStarred.objects.filter(aID=editActor)
                                for j in oldMovies:
                                        j.delete()

                                #Edits the actor information in MovieDB
                                editActor.placeofbirth = st2
                                editActor.dateofbirth = st3
                                editActor.save()

                                #Adds to the Movie-Actor relational table
                                for i in mo:
                                        if len(i) > 0:
                                                i = i[0].capitalize() + i[1:]
                                        try:
                                                addMovie = MovieDB.objects.get(title=i)
                                                try:
                                                        MovieStarred.objects.get(aID=editActor, mID=addMovie)
                                                except MovieStarred.DoesNotExist:
                                                        newMARelation = MovieStarred(aID=editActor, mID=addMovie)
                                                        newMARelation.save()
                                        except MovieDB.DoesNotExist:
                                                continue

                                state = "The actor has been successfully edited in the database."
                        except ActorDB.DoesNotExist:
                                state = "The actor isn't in the database. The edit suggestion will be deleted."
                        actor.delete()
                elif confirm == 'n' or confirm == 'no':
                        actor.delete()
                        state = "The edit of this actor has been refused."
                else:
                        state = "No changes have been made. Please answer correctly 'yes' or 'no' in the previous page."
        return render(request, 'actor_add_end.html', {'state':state, 'title':st1, 'uid':uid})

def news_add(request):
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

	state = ""
	oldNews = ""
	message = ""
	ty = 'news'
	try:
		oldNews = Website.objects.get(typ=ty)
		message = oldNews.message
	except Website.DoesNotExist:
		oldNews = ""
	return render(request, 'news_add.html', {'state':state, 'message':message, 'uid':uid})

def news_add_end(request):
	state = ''
	news = ''
	if request.POST:
		news = request.POST.get('news')
		if news == '':
			state = 'No news has been entered.'
			return render(request, 'error.html', {'state':state})
		else:
			try:
				n = Website.objects.get(typ='news')
				n.message = news
				n.save()
			except Website.DoesNotExist:
				newNews = Website(typ='news', message=news)
				newNews.save()
	return render(request, 'news_add_end.html', {'state':state, 'news':news})

def tv_main(request):
        state = ''
        perm = ''
        uid = 0
        tvs = TVDB.objects.all()
        titles = helper.sort_title(tvs)
        ids = helper.sort_tv_id(tvs, titles)
        if 'username' in request.session:
                uid = request.session['uid']
                user = User.objects.get(username=request.session['username'])
                if user.is_staff:
                        perm = 'a'
                else:
                        perm = 'u'
        if len(ids) == 0:
                state = "No TV shows found in the database."
        return render(request, 'tv_main.html', {'state':state, 'perm':perm, 'ids':ids, 'uid':uid})

def tv_info(request, i):
	state = ''
	st1 = st2 = st3 = st4 = ''
	perm = ''
	uid = 0
	actorList = []
	aIDList = []
	aList = []
	rating = 0
	rat = 0
	if 'username' in request.session:
		uid = request.session['uid']
		user = User.objects.get(username=request.session['username'])
		if user.is_staff:
			perm = 'a'
		else:
			perm = 'u'

	try:
		tv = TVDB.objects.get(id=i)
		st1 = tv.title
		st2 = tv.year
		st3 = tv.season
		st4 = tv.synopsis

		if request.POST:
			if not request.POST.get('rating') == None:
				rat = int(request.POST.get('rating'))
			if rat > 0 and rat < 6:
				try:
					userRating = TVRating.objects.get(username=request.session['username'], tID=tv)
					userRating.rating = rat
					userRating.save()
				except TVRating.DoesNotExist:
					userRating = TVRating(username=request.session['username'], tID=tv, rating=rat)
					userRating.save()
	
		try:
			TVsStarred = TVStarred.objects.filter(tID=tv)
			actors = []
			for l in TVsStarred:
				actors.append(l.aID)
			for k in actors:
				actorList.append(k.name)
			for j in actorList:
				try:
					aid = ActorDB.objects.get(name=j)
					aIDList.append(aid.id)
				except ActorDB.DoesNotExist:
					continue
			for m in range(len(actors)):
				aList.append((str(actorList[m]), str(aIDList[m])))
		except TVStarred.DoesNotExist:
			state = "Possible problem with the relational database."

		try:
			TVRatings = TVRating.objects.filter(tID=tv)
			totalRating = 0
			for j in TVRatings:
				totalRating = totalRating + j.rating
			if len(TVRatings) > 0:
				rating = float(totalRating) / float(len(TVRatings)) 
		except TVRating.DoesNotExist:
			rating = 0	
		try:
                        TVWatchlist.objects.get(username=user, tID=tv)
                        watchlist = 'Remove this TV show from your watchlist'
                except TVWatchlist.DoesNotExist:
                        watchlist = 'Add this TV show from your watchlist'

	except TVDB.DoesNotExist:
		state = "This TV show does not exist in our database."
	return render(request, 'tv_info.html', {'state':state, 'title':st1, 'year':st2, 'season':st3, 'actors':aList, 'synopsis':st4, 'rating':rating, 'watchlist':watchlist, 'perm':perm, 'num':i, 'uid':uid})

def tv_suggest(request):
	state = ''
	uid = 0
	if 'username' in request.session:
		un = str(request.session['username'])
		uid = request.session['uid']
	if not 'username' in request.session:
                state = "You do not have the permissions to suggest a movie."
                return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	return render(request, 'tv_suggest.html', {'state':state, 'uid':uid})

def tv_suggest_confirm(request):
	st1 = st2 = st3 = st5 = st6 = ''
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
		se = request.POST.get('season')
		ac = request.POST.get('actor')
		sy = request.POST.get('synopsis')
		tv = TV_Suggestion(title=ti, year=ye, season=se, actors=ac, synopsis=sy)
		st1 = str(tv.title)
		st2 = str(tv.year)
		st3 = str(tv.season)
		st5 = str(tv.actors)
		st6 = str(tv.synopsis)
		if not ti == '' and not ye == '' and not se == '' and not ac == '' and not sy == '':
			tv.save()
			return render(request, 'tv_suggest_confirm.html', {'title':st1, 'year':st2, 'season':st3, 'actors':st5, 'synopsis':st6, 'uid':uid})
		else:
			state = 'All fields need to be completed when suggesting a TV show.'
			return render(request, 'error.html', {'state':state})

def tv_add(request):
	uid = 0
	if 'username' in request.session:
		uid = request.session['uid']
		user = User.objects.get(username=request.session['username'])
		if not user.is_staff:
			state = "You do not have the permissions to add a TV show."
			return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	else:
		state = "You are not logged in."
		return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	tvs = TV_Suggestion.objects.all()
	li = []
	for i in tvs:
		li.append(i.title)
	return render(request, 'tv_add.html', {'tvs':li, 'uid':uid})

def tv_add_confirm(request, i):
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
	st1 = st2 = st3 = st5 = st6 = ''
	tvs = TV_Suggestion.objects.all()
	if int(i) > len(tvs):
		state = 'The movie does not exist in the suggestion database anymore.'
	else:
		tv = tvs[int(i)-1]
		st1 = str(tv.title)
		st2 = str(tv.year)
		st3 = str(tv.season)
		st5 = str(tv.actors)
		st6 = str(tv.synopsis)
	return render(request, 'tv_add_confirm.html', {'state':state, 'title':st1, 'year':st2, 'season':st3, 'actors':st5, 'synopsis':st6, 'num':i, 'uid':uid})

def tv_add_end(request, i):
	uid = 0
	if 'username' in request.session:
		uid = request.session['uid']
		user = User.objects.get(username=request.session['username'])
		if not user.is_staff:
			state = "You do not have the permissions to add a TV show."
			return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	else:
		state = "You are not logged in."
		return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	state = ''
	st1 = ''
	if request.POST:
		num = int(i)
		li = TV_Suggestion.objects.all()
		confirm = request.POST.get('accept')
		tv = li[num-1]
		st1 = str(tv.title)
		st2 = str(tv.year)
		st3 = str(tv.season)
		st5 = str(tv.actors)
		st6 = str(tv.synopsis)
		if confirm == 'y' or confirm == 'yes':
			#Checks if the movie is already in the database
			try:
				TVDB.objects.get(title=st1)
				state = "The movie is already in the database. The suggestion will be deleted. Please edit the current TV show."
			except TVDB.DoesNotExist:
				ac = st5.split(', ')
				#Checks the relational property of TV-Actor. If the actor is not present, add the actor
				for i in ac:
					if len(i) > 0:
							i = i[0].capitalize() + i[1:]
					try:
						ActorDB.objects.get(name=i)
					except ActorDB.DoesNotExist:
						newActor = ActorDB(name=i)
						newActor.save()
				newTV = TVDB(title=st1, year=st2, season=st3, synopsis=st6)
				newTV.save()
				
				#Adds to the TV-Actor relational table
				for i in ac:
					if len(i) > 0:
						i = i[0].capitalize() + i[1:]
					try:
						addActor = ActorDB.objects.get(name=i)
						try:
							TVStarred.objects.get(tID=newTV, aID=addActor)
						except TVStarred.DoesNotExist:
							newTARelation = TVStarred(tID=newTV, aID=addActor)
							newTARelation.save()
					except TVDB.DoesNotExist:
						continue
				
				state = "The TV show has been successfully added to the database."
			tv.delete()
		elif confirm == 'n' or confirm == 'no':
			tv.delete()
			state = "The addition of this TV show has been refused."
		else:
			state = "No changes have been made. Please answer correctly 'yes' or 'no' in the previous page."
	return render(request, 'tv_add_end.html', {'state':state, 'title':st1, 'uid':uid})

def movie_watchlist(request, i):
	state = ''
	uid = 0
	movie = ''
	title = ''
        if 'username' in request.session:
                uid = request.session['uid']
                user = User.objects.get(username=request.session['username'])
        else:
                state = "You are not logged in."
                return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	try:
		movie = MovieDB.objects.get(id=i)
		title = movie.title
	except MovieDB.DoesNotExist:
		state = 'The movie has not found in the database.'
		return render(request, 'error.html', {'state':state})

	try:
		mwl = MovieWatchlist.objects.get(username=user, mID=movie)
		mwl.delete()
		state = 'The movie has been removed from your watchlist.'
	except MovieWatchlist.DoesNotExist:
		mwl = MovieWatchlist(username=user, mID=movie)
		mwl.save()
		state = 'The movie has been added to your watchlist.'
	return render(request, 'movie_watchlist.html', {'state':state, 'title':title, 'uid':uid})

def tv_watchlist(request, i):
	state = ''
	uid = 0
	tv = ''
	title = ''
	if 'username' in request.session:
		uid = request.session['uid']
		user = User.objects.get(username=request.session['username'])
	else:
		state = 'You are not logged in.'
		return render(request, 'perm_denied.html', {'state':state, 'uid':uid})
	try:
		tv = TVDB.objects.get(id=i)
		title = tv.title
	except TVDB.DoesNotExist:
		state = 'The TV show has not been found in the database.'
		return render(request, 'error.html', {'state':state})

	try:
		twl = TVWatchlist.objects.get(username=user, tID=tv)
		twl.delete()
		state = 'The TV show has been removed from your watchlist.'
	except TVWatchlist.DoesNotExist:
		twl = TVWatchlist(username=user, tID=tv)
		twl.save()
		state = 'The TV show has been added to your watchlist.'
	return render(request, 'tv_watchlist.html', {'state':state, 'title':title})

def help(request):
	state = ''
	perm = ''
	uid = 0
	if 'username' in request.session:
		uid = request.session['uid']
                user = User.objects.get(username=request.session['username'])
                if user.is_staff:
                        perm = 'a'
                else:
                        perm = 'u'
	return render(request, 'help.html', {'state':state, 'perm':perm, 'uid':uid})
