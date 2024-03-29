from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True


# from .models import Course

# class CourseForm(forms.ModelForm):
#     # title = forms.CharField()
#     class Meta:
#         model = Course
#         fields = ['guid', 'title', 'description', 'status']
    
#     def clean_title(self, *args, **kwargs):
#         title = self.cleaned_data.get("title")
#         print(title)
#         if "DJANGO" in title:
#             return title
#         else:
#             raise forms.ValidationError("Not a valid title.")

# class RawForm(forms.Form):
#     guid = forms.CharField()
#     title = forms.CharField()
#     description = forms.CharField()
#     status = forms.BooleanField()

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email',required=True, widget=forms.EmailInput(attrs={'maxlength':150,'placeholder':'Enter Email','autocomplete':'off'}))
    password = forms.CharField(label='Password',required=True,widget= forms.PasswordInput(attrs={'maxlength':150,'placeholder':'Enter Password','autocomplete':'off'}))

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='Email',required=True, widget=forms.EmailInput(attrs={'maxlength':150,'placeholder':'Enter Email','autocomplete':'off'}))
    first_name = forms.CharField(label='First Name',required=False, widget=forms.TextInput(attrs={'maxlength':150,'placeholder':'Enter First Name','autocomplete':'off'}))
    last_name = forms.CharField(label = 'Last Name',required=False, widget=forms.TextInput(attrs={'maxlength':150,'placeholder':'Enter Last Name','autocomplete':'off'}))
    password1 = forms.CharField(label='Password',widget= forms.PasswordInput(attrs={'maxlength':150,'placeholder':'Enter Password','autocomplete':'off'}))
    password2 = forms.CharField(label='Password2',widget= forms.PasswordInput(attrs={'maxlength':150,'placeholder':'Re-enter Password','autocomplete':'off'}))



    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', )
