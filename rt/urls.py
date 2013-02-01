from django.conf.urls import patterns, url

from rt import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^error/$', views.error, name='error'),
	url(r'^login/$', views.login, name='login'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^perm_denied/$', views.perm_denied, name='perm_denied'),
	url(r'^register/$', views.register, name='register'),
	url(r'^register_confirm/$', views.register_confirm, name='register_confirm')
)
