from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Korisnik, Predmeti


# Register your models here.
#admin.site.register(Korisnik)

@admin.register(Korisnik)
class KorisnikAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('None', {'fields':('role', 'status')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('None', {'fields':('role', 'status')}),
    )





# #admin.site.register(Director)

# # Register your models here.



# #admin.site.register(Director)
# admin.site.register(Actor)
# #admin.site.register(Movie)
# #admin.site.register(Role)

# #@admin.register(Director)

# class AdminDirector(admin.ModelAdmin):
#     fields = ('firstname',  'lastname', 'email')
#     #list_display = ('firstname' , 'lastname', 'email')
#     #list_display_links = ('lastname',)
#     #exclude = ('email', 'firstname')
#     #list_editable = ('firstname' , 'email')
#     #classes = ('collapse',)
#     list_filter = ('firstname', 'email')

# admin.site.register(Director, AdminDirector)

# class AdminMovie(admin.ModelAdmin):
#     #list_filter = ('actors','director')
#     #list_filter = ('actors__firstname','director')
#     fields = ('name', 'director', 'actors', 'year', 'genre','parentalguidence' )
#     #radio_fields = {'director':admin.HORIZONTAL}
#     #search_fields = ['actors__firstname']
#     #search_fields = ['name']

# admin.site.register(Movie, AdminMovie)

# class RoleInLine(admin.StackedInline):
#     model = Role
#     can_delete = True
#     verbose_name_plural = 'role'

# class CustomUserAdmin(UserAdmin):
#     inlines = (RoleInLine,)

# admin.site.unregister(User)
# admin.site.register(User,CustomUserAdmin)

 





