from .models import Korisnik
from django.shortcuts import redirect

"""
def decorator(function):
    def wrap(request, *args, **kwargs):
        if SOMETHING:
            return function(request, *args, **kwargs)
        else:
            REJECT
    return wrap
"""

def profesor_required(function):
    def wrap(*args, **kwargs):
        #print(args[0].user)
        #print(args[0].user.role.role)
        if args[0].user.role.role == Korisnik.ROLES[0][0]:
            return function(*args, **kwargs)


        if args[0].user.role.role == Korisnik.ROLES[0][0]:
            return function(*args, **kwargs)
        else:
            return redirect('login')
    return wrap

