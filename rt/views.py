import helper
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rt.models import Movie_Suggestion

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
	return render(request, 'error.html', {})

def perm_denied(request):
	return render(request, 'perm_denied.html', {})
	
def login(request):
	state = ''
	return render(request, 'login.html', {'state':state})	

def logout(request):
	try:
		del request.session['username']
		del request.session['uid']
   	except KeyError:
		state = 'You are currently not logged in.'
		return render(request, 'error.html', {'state':state})
	return render(request, 'logout.html', {})

def register(request):
	state = ''
	if 'username' in request.session:
		state = 'Cannot register when logged in. Please log off first.'
		return render(request, 'perm_denied.html', {'state':state})
	else:
		return render(request, 'register.html', {'state':state})

def register_confirm(request):
	state = 'Registration failed.'
	if request.POST:
		fname = request.POST.get('firstname')
		lname = request.POST.get('lastname')
		email = request.POST.get('email')
		username = request.POST.get('username')
		password = request.POST.get('password')
		cpassword = request.POST.get('confirmPassword')
		if fname == '' or lname == '' or email == '' or username == '' or password == '' or cpassword == '':
			state = 'Information is missing. All fields must be completed.'
			return(request, 'error.html', {'state':state})
		elif helper.user_present(username):
			state = 'The username ' + username + ' is already taken. Please choose another one.'
			return render(request, 'register.html', {'state':state})
		else:
			user = User.objects.create_user(username, email, password)
			user.first_name = fname
			user.last_name = lname
			user.save()
			state = fname + ' ' + lname
			return render(request, 'register_confirm.html', {'state':state})
	return render(request, 'error.html', {'state':state})

def movie_main(request):
	state = ''
	perm = ''
	if 'username' in request.session:
		user = User.objects.get(username=request.session['username'])
		if user.is_staff:
			perm = 'a'
		else:
			perm = 'u'
	return render(request, 'movie_main.html', {'state':state, 'perm':perm})

def movie_suggest(request):
	state = ''
	return render(request, 'movie_suggest.html', {'state':state})

def movie_suggest_confirm(request):
	st1 = st2 = st3 = st4 = st5 = st6 = ''
	if request.POST:
		ti = request.POST.get('title')
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
	return render(request, 'movie_suggest_confirm.html', {'title':st1, 'year':st2, 'director':st3, 'producer':st4, 'actors':st5, 'synopsis':st6})
