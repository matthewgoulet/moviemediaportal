from django.contrib import admin
from rt.models import Movie_Suggestion, Movie_List

class UserAdmin(admin.ModelAdmin):
        fieldsets = [
                ('Title', {'fields': ['title', 'year']}),
                ('Other information', {'fields': ['director', 'producer', 'actors', 'synopsis'], 'classes': ['collapse']}),]

admin.site.register(Movie_Suggestion, UserAdmin)
admin.site.register(Movie_List, UserAdmin)
