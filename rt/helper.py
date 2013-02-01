from django.contrib.auth.models import User

def user_present(username):
	if User.objects.filter(username=username).count():
		return True	
	return False
