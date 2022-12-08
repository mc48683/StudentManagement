from django.forms import ModelForm, PasswordInput
from .models import Predmeti, Korisnik, Upisi
from django import forms
from django.forms import PasswordInput



class PredmetiForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(PredmetiForm, self).__init__(*args, **kwargs)
        self.fields.get('nositelj').queryset = Korisnik.objects.filter(role='prof')
    class Meta:
        exclude=[]
        model = Predmeti


class ProfesorForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
       super(ProfesorForm, self).__init__(*args, **kwargs)
       self.fields['role'].initial="prof"
       self.fields['role'].disabled = True

    class Meta:
        model = Korisnik
        fields = ['username', 'password', 'role']
        help_texts = {
            'username': None,
        }
        widgets = {
            "password": PasswordInput(attrs={'placeholder':'********','autocomplete': 'off','data-toggle': 'password'}),
        }



class StudentForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
       super(StudentForm, self).__init__(*args, **kwargs)
       self.fields['role'].initial="stu"
       self.fields['role'].disabled = True

    class Meta:
        model = Korisnik
        fields = ['username', 'password', 'status', 'role']
        help_texts = {
            'username': None,
        }
        widgets={
        "password": PasswordInput(attrs={'placeholder':'********','autocomplete': 'off','data-toggle': 'password'}),
        }



class UpisiStudentForm(forms.ModelForm):
     class Meta:
        exclude=[]
        model = Upisi
    # student = forms.ForeignKey(Korisnik, on_delete=forms.CASCADE,blank=True, null=True, initial=Korisnik.objects.filter())
    # predmet = forms.ForeignKey(Predmeti, on_delete=forms.CASCADE,blank=True, null=True)
    # status = forms.CharField(default='up', max_length=50, choices=STATUS)


#  class CommentForm(forms.Form):
# ...     name = forms.CharField(initial='Your name')
# ...     url = forms.URLField(initial='http://')
# ...     comment = forms.CharField()
# >>> f = CommentForm(auto_id=False)

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    text_file = forms.FileField()
    #image_file = forms.ImageField()
