from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


# class Role(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     ZAPOSLENIK = 'ZAPOSLENIK'
#     KUPAC =  'KUPAC'
#     VODITELJ  = 'VODITELJ'
#     ROLE_CHOICES = [
#         (KUPAC, 'kupac'),
#         (ZAPOSLENIK, 'zaposlenik'),
#         (VODITELJ, 'voditelj')
#     ]

#     role = models.CharField(choices=ROLE_CHOICES, max_length=50)

#     """ def __str__(self):
#         return '%s %s' % (self.user.username, self.role) """


class Korisnik(AbstractUser):
    ROLES = (('prof', 'profesor'), ('stu', 'student'),('admin','administrator'))
    STATUS = (('none', 'None'), ('izv', 'izvanredni student'), ('red', 'redovni student'))
    role = models.CharField(max_length=50, choices=ROLES)
    status = models.CharField(max_length=50, choices=STATUS)

class Predmeti(models.Model):
    IZBORNI = (('DA', 'da'), ('NE', 'ne'))
    name = models.CharField(max_length=50)
    kod = models.CharField(max_length=50)
    program = models.CharField(max_length=50)
    ects = models.IntegerField()
    sem_red = models.IntegerField()
    sem_izv = models.IntegerField()
    izborni = models.CharField(max_length=50, choices=IZBORNI)
    nositelj = models.ForeignKey(Korisnik, on_delete=models.CASCADE,blank=True, null=True)

    
    def __str__(self):
        return '%s %s' % (self.name, self.kod)



class Upisi(models.Model):
    STATUS = (('up', 'upisan'), ('pol', 'polozen'), ('izg', 'izgubio potpis'))
    student = models.ForeignKey(Korisnik, on_delete=models.CASCADE,blank=True, null=True)
    predmet = models.ForeignKey(Predmeti, on_delete=models.CASCADE,blank=True, null=True)
    status = models.CharField(default='up', max_length=50, choices=STATUS)







