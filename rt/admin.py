from django.contrib import admin
from rt.models import Movie_Suggestion, MovieDB, Actor_Suggestion, ActorDB, MovieStarred

class UserAdmin(admin.ModelAdmin):
	fieldsets = [
		('Title', {'fields': ['title', 'year']}),
		('Other information', {'fields': ['director', 'producer', 'synopsis', 'rating'], 'classes': ['collapse']}),]

admin.site.register(Movie_Suggestion, UserAdmin)
admin.site.register(MovieDB, UserAdmin)

class UserAdmin2(admin.ModelAdmin):
	fieldsets = [
		('Personal information', {'fields': ['name', 'placeofbirth', 'dateofbirth']})]
		
admin.site.register(ActorDB, UserAdmin2)
admin.site.register(Actor_Suggestion, UserAdmin2)

class MovieActorRelation(admin.ModelAdmin):
	fieldsets = [
		('Relation', {'fields': ['mID', 'aID']})]
		
admin.site.register(MovieStarred, MovieActorRelation)
