from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

from rt import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^error/$', views.error, name='error'),
	url(r'^login/$', views.login, name='login'),
	url(r'^actor/$', views.actor_main, name='actor_main'),
	url(r'^actor/(?P<i>\d+)/$', views.actor_info, name='actor_info'),
	url(r'^actor/add/$', views.actor_add, name='actor_add'),
	url(r'^actor/add/(?P<i>\d+)/$', views.actor_add_confirm, name='actor_add_confirm'),
	url(r'^actor/add/(?P<i>\d+)/confirm/$', views.actor_add_end, name='actor_add_end'),
	url(r'^actor_suggest/$', views.actor_suggest, name='actor_suggest'),
	url(r'^actor_suggest/confirm/$', views.actor_suggest_confirm, name='actor_suggest_confirm'),
	url(r'^movie/$', views.movie_main, name='movie_main'),
	url(r'^movie/(?P<i>\d+)/$', views.movie_info, name='movie_info'),
	url(r'^movie/add/$', views.movie_add, name='movie_add'),
	url(r'^movie/add/(?P<i>\d+)/$', views.movie_add_confirm, name='movie_add_confirm'),
	url(r'^movie/add/(?P<i>\d+)/confirm/$', views.movie_add_end, name='movie_add_end'),
	url(r'^movie/(?P<i>\d+)/delete/$', views.movie_delete, name='movie_delete'),
	url(r'^movie/(?P<i>\d+)/delete/confirm/$', views.movie_delete_confirm, name='movie_delete_confirm'),
	url(r'^movie_suggest/$', views.movie_suggest, name='movie_suggest'),
	url(r'^movie_suggest/confirm/$', views.movie_suggest_confirm, name='movie_suggest_confirm'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^perm_denied/$', views.perm_denied, name='perm_denied'),
	url(r'^register/$', views.register, name='register'),
	url(r'^register_confirm/$', views.register_confirm, name='register_confirm')
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
