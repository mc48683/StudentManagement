"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('insert_predmet/', views.add_predmeti, name="insert_predmet"),
    path('upisnilist/', views.get_predmeti, name='predmeti'),
    path('welcome/', views.welcome),
    path('login/', LoginView.as_view(template_name='login.html'), name='login_page'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('prof/', views.prof_predmeti, name='prof_predmeti'),
    path('details/<int:predmet_id>',views.details, name="details"),
    path("",views.details, name="details"),
    path('administrator/',views.administrator, name="administrator"),
    path('admin_predmeti/',views.admin_predmeti,name="admin_predmeti"),
    path('admin_prof/',views.admin_prof,name="admin_prof"),
    path('admin_studenti/',views.admin_studenti,name="admin_studenti"),
    path('insert_student/', views.add_studenti, name="insert_student"),
    path('insert_profesor/', views.add_profesori, name="insert_profesor"),
    path('edit_profesor/<int:prof_id>', views.edit_profesor, name="edit_profesor"),
    path('edit_student/<int:student_id>', views.edit_student, name="edit_student"),
    path('edit_predmet/<int:predmet_id>', views.edit_predmet, name="edit_predmet"),
    path('popis_studenata/<int:predmet_id>', views.popis_studenata, name="popis_studenata"),
    #path('upload/', views.upload_file, name='upload'),
    path('polozeno/<int:upis_id>',views.polozio,name="polozeno"),
    path('izgubio/<int:upis_id>',views.izgubio,name="izgubio"),
    path('ispisi/<int:upis_id>',views.ispisi,name="ispisi"),
    path('confirm_ispis/<int:upis_id>', views.confirm_ispis, name='confirm_ispis'),
    path('student/', views.student, name='student'),
    path('student_izv/', views.student_izv, name='student_izv'),
    path('student_red/', views.student_red, name='student_red'),
    path('upisni_list_izv/', views.upisni_list_izv, name='upisni_list_izv'),
    path('upisni_list_red/', views.upisni_list_red, name='upisni_list_red'),
    path('upisni_list/<int:student_id>', views.upisni_list, name='upisni_list'),
    path('upisi/<int:predmet_id>', views.upisi, name='upisi'),
    path('upisi_admin/<int:predmet_id>/<int:student_id>',views.upisi_admin,name='upisi_admin'),
    path('ispisi_predmet/<int:upis_id>/', views.ispisi_predmet, name='ispisi_predmet'),
    path('navigation/',views.navigation,name="navigation"),
    path('ects/',views.ects,name="ects"),
    path('polozeni/',views.polozeni,name="polozeni"),
]
