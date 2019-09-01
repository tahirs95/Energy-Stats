from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.urls import reverse
from django.http import Http404
from django.contrib import messages
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import(
    ListView
)
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, LoginForm
from django.contrib.auth.models import User

from django.contrib.auth import login, authenticate, logout

@login_required(login_url='/login/')
def home(request ,*args, **kwargs):
    print(request.user)
    # return HttpResponse("<h1> Hello World </h1>")
    dict_new = {"guid":"121131313", "name":"Django and Python", "status":True, "html":"<i>Hifari<i>"}
    return render(request, "home.html", {'dict':dict_new})

@csrf_exempt
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            userName = str(new_user.first_name) + ' ' + str(new_user.last_name)
            new_user.username = userName
            form.save()
            return redirect('/survey/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {
        'form':form
    })

@csrf_exempt
def user_login(request):
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            email = form_data['email']
            usr = User.objects.filter(email=email)
            if len(usr)>0:
                usr = User.objects.get(email = email)
                username = usr.username
            user = authenticate(request, username=username, password=form_data['password'])
            print(user)
            if user is not None:
                login(request,user)
                messages.success(request, "Authenticated Successfully.")
                print("pass")
                return redirect("/survey/")
            else:
                print("fail")
                messages.error(request, "Invalid login.")
                return redirect('registration/login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html',{'form':form})