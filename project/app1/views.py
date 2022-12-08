
from asyncore import poll3
from pickletools import read_long1
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.contrib.auth.decorators import login_required 
from .models import Korisnik, Predmeti, Upisi
from .forms import PredmetiForm, UpisiStudentForm, StudentForm, ProfesorForm, UploadFileForm
from django.contrib.auth.hashers import make_password
from django.core.files.storage import FileSystemStorage

from .decorators import profesor_required

def navigation(request):
    current_user=request.user
    if current_user.role=="prof":
        return redirect('prof_predmeti')
    elif current_user.role=="admin":
        return redirect('administrator')
    else:
        return redirect('student')


def register(request):
    if request.method == 'GET':
        userForm = UserCreationForm()
        return render(request, 'register.html', {'form':userForm})
    elif request.method == 'POST':
        userForm = UserCreationForm(request.POST)
        if userForm.is_valid():
            userForm.save()
            print("")
            print("***")
            print(userForm)
            print("")
            print("***")
            cleaned_data = userForm.cleaned_data
            print(cleaned_data)
            print("")
            print("***")
            return redirect('login')
        else:
            return redirect('register')
    else:
        return HttpResponseNotAllowed('Not able to save!')



def add_predmeti(request):
    print('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if request.method == 'GET':
        predmetiForm = PredmetiForm()
        return render(request, 'insert_predmet.html', {'form':predmetiForm.as_table()})
    elif request.method == 'POST':
        predmetiForm = PredmetiForm(request.POST)
        if predmetiForm.is_valid():
            predmetiForm.save()
            cleaned_data = predmetiForm.cleaned_data
            print(cleaned_data)
            return redirect('admin_predmeti')            
        else:
            return HttpResponseNotAllowed(["POST"])
    return redirect('login')
    #return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))



def add_profesori(request):
    print('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if request.method == 'GET':
        profesorForm = ProfesorForm()
        return render(request, 'insert_profesor.html', {'form':profesorForm.as_table()})
    elif request.method == 'POST':
        profesorForm = ProfesorForm(request.POST)
        if profesorForm.is_valid():
            sign_up = profesorForm.save()
            sign_up.password = make_password(profesorForm.cleaned_data['password'])
            sign_up.save()
            return redirect('admin_prof')            
        else:
            return HttpResponseNotAllowed(["POST"])
    return redirect('login')


def add_studenti(request):
    print('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if request.method == 'GET':
        studentiForm = StudentForm()
        return render(request, 'insert_student.html', {'form':studentiForm.as_table()})
    elif request.method == 'POST':
        studentiForm = StudentForm(request.POST)
        if studentiForm.is_valid():
            sign_up = studentiForm.save()
            sign_up.password = make_password(studentiForm.cleaned_data['password'])
            sign_up.save()
            return redirect('admin_studenti')            
        else:
            return HttpResponseNotAllowed(["POST"])
    return redirect('login')


def edit_profesor(request, prof_id):           
    prof_by_id = Korisnik.objects.get(id=prof_id)
    if request.method == 'GET':
        data_to_update = ProfesorForm(instance=prof_by_id)
        return render(request, 'edit_profesor.html', {'form': data_to_update})
    elif request.method == 'POST':
        print(request.POST)
        data_to_update = ProfesorForm(request.POST, instance=prof_by_id)
        if data_to_update.is_valid():
            data_to_update.save()
            return redirect('admin_prof')
    else:
        return HttpResponse("Something went wrong!")



def edit_student(request, student_id):           
    student_by_id = Korisnik.objects.get(id=student_id)
    if request.method == 'GET':
        data_to_update = StudentForm(instance=student_by_id)
        return render(request, 'edit_student.html', {'form': data_to_update})
    elif request.method == 'POST':
        print(request.POST)
        data_to_update = StudentForm(request.POST, instance=student_by_id)
        if data_to_update.is_valid():
            data_to_update.save()
            return redirect('admin_studenti')
    else:
        return HttpResponse("Something went wrong!")



def edit_predmet(request, predmet_id):           
    predmet_by_id = Predmeti.objects.get(id=predmet_id)
    if request.method == 'GET':
        data_to_update = PredmetiForm(instance=predmet_by_id)
        return render(request, 'edit_predmet.html', {'form': data_to_update})
    elif request.method == 'POST':
        print(request.POST)
        data_to_update = PredmetiForm(request.POST, instance=predmet_by_id)
        if data_to_update.is_valid():
            data_to_update.save()
            return redirect('admin_predmeti')
    else:
        return HttpResponse("Something went wrong!")


def popis_studenata(request, predmet_id):
    predmet_by_id = Predmeti.objects.get(id=predmet_id)
    upis=Upisi.objects.filter(predmet_id=predmet_by_id)
    j=0
    list1=[]
    list=[]
    
    for i in upis:
        korisnik=Korisnik.objects.filter(id=upis[j].student_id)
        list1.append(i)
#upis=Upisi.objects.filter(id=upisi[j].student_id)
        #list2.append(upis)
        #list.append(korisnik)
        j=j+1  
        list.append(korisnik) 
    zip1=zip(list,list1)
    return render(request, 'popis_studenata.html', {"data":list,"data1":list1,"zip1":zip1})

def welcome(request):
    return HttpResponse("<b>Hello World!</b>")


def get_predmeti(request):
    i=1
    while i<9:
        predmeti = Predmeti.objects.filter(sem_red=i)
        i=i-1
        return render(request, 'upisni_list.html', {"data":predmeti})


def prof_predmeti(request):
    current_user = request.user
    nositelj_id = current_user.id
    predmet = Predmeti.objects.filter(nositelj_id=nositelj_id)

    d5 = Upisi(7,4,36,status="up")
    d5.save()
    return render(request, 'prof.html', {"data":predmet})

def administrator(request):
     return render(request, 'administrator.html')


def ects(request):
    current_user = request.user
    predmeti=Predmeti.objects.all()
    ects=[]
    zbroj=0
    upisani=[]
    upisi=Upisi.objects.filter(student_id=current_user.id)
    for i in upisi:
        if i.status=="up":
            upisani.append(i)
    for i in upisani:
        for j in predmeti:
            if i.predmet_id==j.id:
                ects.append(j)
                zbroj=zbroj+j.ects
    

    return render(request, 'ects.html',{"data":ects,"zbroj":zbroj})


def polozeni(request):
    current_user = request.user
    predmeti=Predmeti.objects.all()
    ects=[]
    zbroj=0
    polozeni=[]
    upisi=Upisi.objects.filter(student_id=current_user.id)
    for i in upisi:
        if i.status=="pol":
            polozeni.append(i)
    for i in polozeni:
        for j in predmeti:
            if i.predmet_id==j.id:
                ects.append(j)
                zbroj=zbroj+j.ects
    return render(request, 'polozeni.html',{"data":ects,"zbroj":zbroj})


def upisni_list(request,student_id):
    student=Korisnik.objects.get(id=student_id)
    ostali=[]
    zip1=[]
    zip2=[]
    zip3=[]
    zip4=[]
    zip5=[]
    zip6=[]
    zip7=[]
    zip8=[]
    up1=[]
    pol1=[]
    upis1=[]
    up2=[]
    pol2=[]
    upis2=[]
    up3=[]
    pol3=[]
    upis3=[]
    up4=[]
    pol4=[]
    upis4=[]
    up5=[]
    pol5=[]
    upis5=[]
    up6=[]
    pol6=[]
    upis6=[]
    up7=[]
    pol7=[]
    upis7=[]
    up8=[]
    pol8=[]
    upis8=[]
    if student.status=="izv":
        predmeti=Predmeti.objects.all()
        upisi=Upisi.objects.filter(student_id=student.id)
        flag=True
        for i in predmeti:
            flag=True
            for j in upisi:
                if j.predmet_id == i.id:
                    flag=False
            if flag==True:
                ostali.append(i)
        #d5 = Upisi(10,40,3,status="pol")
        #d5.save()
        izv1=Predmeti.objects.filter(sem_izv=1)
        for i in izv1:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up1.append(i)
                        upis1.append(j)
                        zip1=zip(up1,upis1)
                    elif j.status=="pol":
                        pol1.append(i)
        izv2=Predmeti.objects.filter(sem_izv=2)
        for i in izv2:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up2.append(i)
                        upis2.append(j)
                        zip2=zip(up2,upis2)
                    elif j.status=="pol":
                        pol2.append(i)

        izv3=Predmeti.objects.filter(sem_izv=3)
        for i in izv3:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up3.append(i)
                        upis3.append(j)
                        zip3=zip(up3,upis3)
                    elif j.status=="pol":
                        pol3.append(i)

        izv4=Predmeti.objects.filter(sem_izv=4)
        for i in izv4:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up4.append(i)
                        upis4.append(j)
                        zip4=zip(up4,upis4)
                    elif j.status=="pol":
                        pol4.append(i)

        izv5=Predmeti.objects.filter(sem_izv=5)
        for i in izv5:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up5.append(i)
                        upis5.append(j)
                        zip5=zip(up5,upis5)
                    elif j.status=="pol":
                        pol5.append(i)

        izv6=Predmeti.objects.filter(sem_izv=6)
        for i in izv6:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up6.append(i)
                        upis6.append(j)
                        zip6=zip(up6,upis6)
                    elif j.status=="pol":
                        pol6.append(i)

        izv7=Predmeti.objects.filter(sem_izv=7)
        for i in izv7:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up7.append(i)
                        upis7.append(j)
                        zip7=zip(up7,upis7)
                    elif j.status=="pol":
                        pol7.append(i)

        izv8=Predmeti.objects.filter(sem_izv=8)
        for i in izv8:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up8.append(i)
                        upis8.append(j)
                        zip8=zip(up8,upis8)
                    elif j.status=="pol":
                        pol8.append(i)

        return render(request, 'upisni_list_izv.html',{"student_id":student_id,"zip1":zip1,"zip2":zip2,"zip3":zip3,"zip4":zip4,"zip5":zip5,"zip6":zip6,"zip7":zip7,"zip8":zip8,"all":ostali,"up1":up1,"pol1":pol1,"up2":up2,"pol2":pol2,"up3":up3,"pol3":pol3,"up4":up4,"pol4":pol4,"up5":up5,"pol5":pol5,"up6":up6,"pol6":pol6,"up7":up7,"pol7":pol7,"up8":up8,"pol8":pol8,"upis1":upis1,"upis2":upis2,"upis3":upis3,"upis4":upis4,"upis5":upis5,"upis6":upis6,"upis7":upis7,"upis8":upis8})
    elif student.status=="red":
        upisi=Upisi.objects.filter(student_id=student.id)
        predmeti=Predmeti.objects.all()
        flag=True
        for i in predmeti:
            flag=True
            for j in upisi:
                if j.predmet_id == i.id:
                    flag=False
            if flag==True:
                ostali.append(i)
        
        red1=Predmeti.objects.filter(sem_red=1)
        for i in red1:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up1.append(i)
                        upis1.append(j)
                        zip1=zip(up1,upis1)
                    elif j.status=="pol":
                        pol1.append(i)

        red2=Predmeti.objects.filter(sem_red=2)
        for i in red2:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up2.append(i)
                        upis2.append(j)
                        zip2=zip(up2,upis2)
                    elif j.status=="pol":
                        pol2.append(i)

        red3=Predmeti.objects.filter(sem_red=3)
        for i in red3:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up3.append(i)
                        upis3.append(j)
                        zip3=zip(up3,upis3)
                    elif j.status=="pol":
                        pol3.append(i)

        red4=Predmeti.objects.filter(sem_red=4)
        for i in red4:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up4.append(i)
                        upis4.append(j)
                        zip4=zip(up4,upis4)
                    elif j.status=="pol":
                        pol4.append(i)

        red5=Predmeti.objects.filter(sem_red=5)
        for i in red5:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up5.append(i)
                        upis5.append(j)
                        zip5=zip(up5,upis5)
                    elif j.status=="pol":
                        pol5.append(i)

        red6=Predmeti.objects.filter(sem_red=6)
        for i in red6:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up6.append(i)
                        upis6.append(j)
                        zip6=zip(up6,upis6)
                    elif j.status=="pol":
                        pol6.append(i)

        return render(request, 'upisni_list_red.html',{"student_id":student_id,"zip1":zip1,"zip2":zip2,"zip3":zip3,"zip4":zip4,"zip5":zip5,"zip6":zip6,"all":ostali,"up1":up1,"pol1":pol1,"up2":up2,"pol2":pol2,"up3":up3,"pol3":pol3,"up4":up4,"pol4":pol4,"up5":up5,"pol5":pol5,"up6":up6,"pol6":pol6,"upis1":upis1,"upis2":upis2,"upis3":upis3,"upis4":upis4,"upis5":upis5,"upis6":upis6})
    return render(request, 'login.html')
def student(request):
    current_user = request.user
    ostali=[]
    zip1=[]
    zip2=[]
    zip3=[]
    zip4=[]
    zip5=[]
    zip6=[]
    zip7=[]
    zip8=[]
    up1=[]
    pol1=[]
    upis1=[]
    up2=[]
    pol2=[]
    upis2=[]
    up3=[]
    pol3=[]
    upis3=[]
    up4=[]
    pol4=[]
    upis4=[]
    up5=[]
    pol5=[]
    upis5=[]
    up6=[]
    pol6=[]
    upis6=[]
    up7=[]
    pol7=[]
    upis7=[]
    up8=[]
    pol8=[]
    upis8=[]
    if current_user.status=="izv":
        predmeti=Predmeti.objects.all()
        upisi=Upisi.objects.filter(student_id=current_user.id)
        flag=True
        for i in predmeti:
            flag=True
            for j in upisi:
                if j.predmet_id == i.id:
                    flag=False
            if flag==True:
                ostali.append(i)
        #d5 = Upisi(10,40,3,status="pol")
        #d5.save()
        izv1=Predmeti.objects.filter(sem_izv=1)
        for i in izv1:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up1.append(i)
                        upis1.append(j)
                        zip1=zip(up1,upis1)
                    elif j.status=="pol":
                        pol1.append(i)
        izv2=Predmeti.objects.filter(sem_izv=2)
        for i in izv2:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up2.append(i)
                        upis2.append(j)
                        zip2=zip(up2,upis2)
                    elif j.status=="pol":
                        pol2.append(i)

        izv3=Predmeti.objects.filter(sem_izv=3)
        for i in izv3:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up3.append(i)
                        upis3.append(j)
                        zip3=zip(up3,upis3)
                    elif j.status=="pol":
                        pol3.append(i)

        izv4=Predmeti.objects.filter(sem_izv=4)
        for i in izv4:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up4.append(i)
                        upis4.append(j)
                        zip4=zip(up4,upis4)
                    elif j.status=="pol":
                        pol4.append(i)

        izv5=Predmeti.objects.filter(sem_izv=5)
        for i in izv5:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up5.append(i)
                        upis5.append(j)
                        zip5=zip(up5,upis5)
                    elif j.status=="pol":
                        pol5.append(i)

        izv6=Predmeti.objects.filter(sem_izv=6)
        for i in izv6:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up6.append(i)
                        upis6.append(j)
                        zip6=zip(up6,upis6)
                    elif j.status=="pol":
                        pol6.append(i)

        izv7=Predmeti.objects.filter(sem_izv=7)
        for i in izv7:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up7.append(i)
                        upis7.append(j)
                        zip7=zip(up7,upis7)
                    elif j.status=="pol":
                        pol7.append(i)

        izv8=Predmeti.objects.filter(sem_izv=8)
        for i in izv8:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up8.append(i)
                        upis8.append(j)
                        zip8=zip(up8,upis8)
                    elif j.status=="pol":
                        pol8.append(i)

        return render(request, 'student_izv.html',{"zip1":zip1,"zip2":zip2,"zip3":zip3,"zip4":zip4,"zip5":zip5,"zip6":zip6,"zip7":zip7,"zip8":zip8,"data":current_user,"all":ostali,"up1":up1,"pol1":pol1,"up2":up2,"pol2":pol2,"up3":up3,"pol3":pol3,"up4":up4,"pol4":pol4,"up5":up5,"pol5":pol5,"up6":up6,"pol6":pol6,"up7":up7,"pol7":pol7,"up8":up8,"pol8":pol8,"upis1":upis1,"upis2":upis2,"upis3":upis3,"upis4":upis4,"upis5":upis5,"upis6":upis6,"upis7":upis7,"upis8":upis8})
    elif current_user.status=="red":
        upisi=Upisi.objects.filter(student_id=current_user.id)
        predmeti=Predmeti.objects.all()
        flag=True
        for i in predmeti:
            flag=True
            for j in upisi:
                if j.predmet_id == i.id:
                    flag=False
            if flag==True:
                ostali.append(i)
        
        red1=Predmeti.objects.filter(sem_red=1)
        for i in red1:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up1.append(i)
                        upis1.append(j)
                        zip1=zip(up1,upis1)
                    elif j.status=="pol":
                        pol1.append(i)

        red2=Predmeti.objects.filter(sem_red=2)
        for i in red2:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up2.append(i)
                        upis2.append(j)
                        zip2=zip(up2,upis2)
                    elif j.status=="pol":
                        pol2.append(i)

        red3=Predmeti.objects.filter(sem_red=3)
        for i in red3:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up3.append(i)
                        upis3.append(j)
                        zip3=zip(up3,upis3)
                    elif j.status=="pol":
                        pol3.append(i)

        red4=Predmeti.objects.filter(sem_red=4)
        for i in red4:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up4.append(i)
                        upis4.append(j)
                        zip4=zip(up4,upis4)
                    elif j.status=="pol":
                        pol4.append(i)

        red5=Predmeti.objects.filter(sem_red=5)
        for i in red5:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up5.append(i)
                        upis5.append(j)
                        zip5=zip(up5,upis5)
                    elif j.status=="pol":
                        pol5.append(i)

        red6=Predmeti.objects.filter(sem_red=6)
        for i in red6:
            for j in upisi:
                if i.id==j.predmet_id:
                    if j.status=="up":
                        up6.append(i)
                        upis6.append(j)
                        zip6=zip(up6,upis6)
                    elif j.status=="pol":
                        pol6.append(i)

        return render(request, 'student_red.html',{"zip1":zip1,"zip2":zip2,"zip3":zip3,"zip4":zip4,"zip5":zip5,"zip6":zip6,"data":current_user,"all":ostali,"up1":up1,"pol1":pol1,"up2":up2,"pol2":pol2,"up3":up3,"pol3":pol3,"up4":up4,"pol4":pol4,"up5":up5,"pol5":pol5,"up6":up6,"pol6":pol6,"upis1":upis1,"upis2":upis2,"upis3":upis3,"upis4":upis4,"upis5":upis5,"upis6":upis6})
    return render(request, 'login.html')


def upisni_list_izv(request):
    return render(request,'upisni_list_izv.html')

def upisni_list_red(request):
    return render(request,'upisni_list_red.html')


def student_izv(request):
    return render(request,'student_izv.html')

def student_red(request):
    return render(request,'student_red.html')

def admin_predmeti(request):
     predmet = Predmeti.objects.all()
     return render(request, 'admin_predmeti.html', {"data":predmet})


def admin_prof(request):
     prof = Korisnik.objects.filter(role="prof")
     return render(request, 'admin_prof.html', {"data":prof})


def admin_studenti(request):
     student = Korisnik.objects.filter(role="stu")
     return render(request, 'admin_studenti.html', {"data":student})


#@profesor_required
def details(request, predmet_id):
    upisi = Upisi.objects.filter(predmet_id=predmet_id)
    predmet = Predmeti.objects.filter(id=predmet_id)
    ostali=[]
    ostali_user=[]
    pol=[]
    pol_user=[]
    izg_user=[]
    izg=[]

    for i in upisi:
        if i.status=="pol":
            pol.append(i)
            user=Korisnik.objects.get(id=i.student_id)
            pol_user.append(user)
        elif i.status=="izg":
            izg.append(i)
            user=Korisnik.objects.get(id=i.student_id)
            izg_user.append(user)
        else:
            ostali.append(i)
            user=Korisnik.objects.get(id=i.student_id)
            ostali_user.append(user)

    zip1=zip(pol,pol_user)
    zip2=zip(izg,izg_user)
    zip3=zip(ostali,ostali_user)
    return render(request, 'details.html',{"data":zip1,"data":zip1,"zip2":zip2,"zip3":zip3,"ime":predmet,"data2":upisi,"pol":pol,"pol_user":pol_user,"izg":izg,"ostali":ostali})




def upisi(request, predmet_id):
    current_user = request.user
    upisi=Upisi.objects.all()
    zbroj=0
    upis2=Upisi.objects.filter(student_id=current_user.id)
    predmet_curr=Predmeti.objects.get(id=predmet_id)
    polozeni=[]
    predmeti=[]
    j=0
    
    for i in upis2:
        if i.status=="pol":
            polozeni.append(i)


    for i in upisi:
        if i.predmet_id==predmet_id and i.student_id==current_user.id:
                    return HttpResponse("Već ste upisali ovaj predmet!")
    

    for i in polozeni:
        predmeti.append(Predmeti.objects.get(id=i.predmet_id))

    
    if current_user.status=="red":
        zbroj=0
        prosli_sem=predmet_curr.sem_red-1
        for i in predmeti:
            if i.sem_red==prosli_sem:
                zbroj=zbroj+i.ects
        if zbroj<10:
            return HttpResponse("Imate manje od 10 ects bodova u prošlom semestru")

    elif current_user.status=="izv":
        prosli_sem=predmet_curr.sem_izv-1
        for i in predmeti:
            if i.sem_izv==prosli_sem:
                zbroj=zbroj+i.ects
        if zbroj<10:
            return HttpResponse("Imate manje od 10 ects bodova u prošlom semestru")

    elif request.method == 'GET':
        return render(request, 'upisi.html')
    elif request.method == 'POST':
        print(request.POST)
        new = Upisi(student=Korisnik.objects.get(id=current_user.id),predmet=Predmeti.objects.get(id=predmet_id),status="up")
        new.save()
        return redirect('student')
    else:
        return HttpResponse("Something went wrong!")






def upisi_admin(request, predmet_id,student_id):
    if request.method == 'GET':
        return render(request, 'upisi.html')
    elif request.method == 'POST':
        print(request.POST)
        new = Upisi(student=Korisnik.objects.get(id=student_id),predmet=Predmeti.objects.get(id=predmet_id),status="up")
        new.save()
        return redirect('admin_studenti')
    else:
        return HttpResponse("Something went wrong!")

def ispisi_predmet(request, upis_id):
    upis_by_id = Upisi.objects.get(id=upis_id)
    print(request.POST)
    if 'da' in request.POST:
        upis_by_id.delete()
        return HttpResponse('Successfully deleted!')
    return redirect('student')


def add_predmeti(request):
    print('%s?next=%s' % (settings.LOGIN_URL, request.path))
    if request.method == 'GET':
        predmetiForm = PredmetiForm()
        return render(request, 'insert_predmet.html', {'form':predmetiForm.as_table()})
    elif request.method == 'POST':
        predmetiForm = PredmetiForm(request.POST)
        if predmetiForm.is_valid():
            predmetiForm.save()
            cleaned_data = predmetiForm.cleaned_data
            print(cleaned_data)
            return redirect('admin_predmeti')            
        else:
            return HttpResponseNotAllowed(["POST"])
    return redirect('login')



def polozio(request, upis_id):
    upis_by_id = Upisi.objects.get(id=upis_id)
    predmet_id=upis_by_id.predmet_id
    if request.method == 'GET':
        return render(request, 'polozeno.html')
    elif request.method == 'POST':
        print(request.POST)
        upis_by_id.status="pol"
        upis_by_id.save()
        return redirect('prof_predmeti')
    else:
        return HttpResponse("Something went wrong!")



def izgubio(request, upis_id):
    upis_by_id = Upisi.objects.get(id=upis_id)
    predmet_id=upis_by_id.predmet_id
    if request.method == 'GET':
        return render(request, 'izgubio.html')
    elif request.method == 'POST':
        print(request.POST)
        upis_by_id.status="izg"
        upis_by_id.save()
        return redirect('prof_predmeti')
    else:
        return HttpResponse("Something went wrong!")

def ispisi(request, upis_id):
    upis_by_id = Upisi.objects.get(id=upis_id)
    print(request.POST)
    if 'da' in request.POST:
        upis_by_id.delete()
        return HttpResponse('Successfully deleted!')
    return redirect('prof_predmeti')


def confirm_ispis(request, upis_id):
    if request.method == 'GET':
        return render(request, 'confirm_ispis.html', {"data":upis_id})
    return HttpResponseNotAllowed()
 

def upload_file(request):
    form = UploadFileForm()
    if request.method == 'GET':
        #form = UploadFileForm()
        print('blaaaa')
        #print(request.FILES['text_file'])
    elif request.method == 'POST':
        FileSystemStorage().save(request.FILES['text_file'].name, request.FILES['text_file'])
    return render(request,'upload.html', {'form':form})