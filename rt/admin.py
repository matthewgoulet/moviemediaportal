from django.contrib import admin
from rt.models import Movie

class UserAdmin(admin.ModelAdmin):
        fieldsets = [
                ('Title', {'fields': ['title', 'year']}),
                ('Other information', {'fields': ['director', 'actors', 'synopsis'], 'classes': ['collapse']}),]

admin.site.register(Movie, UserAdmin)
