from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .forms import SignUpForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from .models import Building, Use, Bill, Option
import json
import random
from django.core.mail import send_mail
from django.conf import settings

def home(request ,*args, **kwargs):
    print(request.user)
    return render(request, "home.html")

def home1(request ,*args, **kwargs):
    print(request.user)
    return render(request, "home1.html")

@csrf_exempt
def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password1'])
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
                usr = User.objects.get(email=email)
                username = usr.username
            user = authenticate(request, username=username, password=form_data['password'])
            if user is not None:
                login(request,user)
                messages.success(request, "Authenticated Successfully.")
                print("pass")
                return redirect("/survey/")
            else:
                print("fail")
                messages.error(request, "Email or Password is incorrect.")
                return redirect('/login/')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html',{'form':form})

# @login_required(login_url='/login/')
def get_buildings(request ,*args, **kwargs):
    building_dict = {}
    if request.user.is_anonymous == False:
        user = request.user
    else:
        user = User.objects.get(email="anonymous@yahoo.com")
    print(user)
    buildings = Building.objects.filter(user=user)
    for i, building in enumerate(buildings):
        building_dict[i] = {}
        building_dict[i]["user"] = building.user.username
        building_dict[i]["title"] = building.title
        building_dict[i]["building_name"] = building.building_name
        building_dict[i]["address"] = building.address
        building_dict[i]["square_footage"] = building.square_footage
        building_dict[i]["uses"] = {}
        for x in building.uses.all():
            building_dict[i]["uses"][x.uses] = x.use_num

        building_dict[i]["applicable_options"] = [x.options for x in building.applicable_options.all()]
        building_dict[i]["electricity_provider"] = building.electricity_provider
        building_dict[i]["group"] = building.group
        building_dict[i]["aggregated_bills"] = [x.bills for x in building.aggregated_bills.all()]
        building_dict[i]["co2_current"] = building.co2_current
        building_dict[i]["co2_2024"] = building.co2_2024
        building_dict[i]["co2_2030"] = building.co2_2030
        building_dict[i]["page"] = building.page
    return JsonResponse({'dict':building_dict})


@csrf_exempt
def add_buildings(request):
    request_data = json.loads(request.body)

    # loading request data
    page = request_data["page"]
    if request.user.is_anonymous == False:
        user = request.user
        print(user)

    if "title" in request_data:

        if request.user.is_anonymous == True:
            random_id = random.randint(0, 10000)
            user = User.objects.create(email="anonymous{}@yahoo.com".format(random_id), username="Anonymous{}".format(random_id))

        title = request_data["title"]
        building_name = request_data["building_name"]
        address = request_data["address"]
        square_footage = request_data["square_footage"]
        uses = request_data["uses"]
        applicable_options = request_data["applicable_options"]
        electricity_provider = request_data["electricity_provider"]

        row = Building.objects.create(
            user=user,
            title=title,
            building_name=building_name,
            address=address,
            square_footage=square_footage,
            electricity_provider=electricity_provider,
            page=page
            )
        
        for applicable_option in applicable_options:
            option_row = Option.objects.create(options=applicable_option)
            row.applicable_options.add(option_row)

        for use_dict in uses:
            use_row = Use.objects.create(uses=use_dict["name"])
            use_row.use_num = use_dict["num"]
            use_row.save()
            row.uses.add(use_row)
        
        if request.user.is_anonymous == True:
            return JsonResponse({"status":"True", "user":user.email ,"message":"Building has been added."})
        else:
            return JsonResponse({"status":"True", "message":"Building has been added."})
    
    elif "group" in request_data:

        if request.user.is_anonymous == True:
            user_email = request_data["user_email"]
            user = User.objects.get(email=user_email)
        building = Building.objects.get(user=user)
        group = request_data["group"]
        building.group = group
        building.page = page
        building.save()

        return JsonResponse({"status":"True", "message":"Building has been edited."})
    
    elif "aggregated_bills" in request_data:

        if request.user.is_anonymous == True:
            user_email = request_data["user_email"]
            user = User.objects.get(email=user_email)
        
        building = Building.objects.get(user=user)
        aggregated_bills = request_data["aggregated_bills"]
        co2_current = request_data["co2_current"]
        co2_2024 = request_data["co2_2024"]
        co2_2030 = request_data["co2_2030"]
        building.co2_current = co2_current
        building.co2_2024 = co2_2024
        building.co2_2030 = co2_2030
        building.page = page
        building.save()
    
        building.aggregated_bills.clear()

        for bill in aggregated_bills:
            use_row = Bill.objects.create(bills=bill)
            building.aggregated_bills.add(use_row)

        return JsonResponse({"status":"True", "message":"Building has been edited."})
    
    else:
        return JsonResponse({"status":"False", "message":"Invalid Request data."})

@csrf_exempt
def email(request):
    print(request.user)
    if request.user.is_anonymous == True:
        request_data = json.loads(request.body)
        email = request_data["email"]
    else:
        email = request.user.email

    subject = 'Thank you for registering to our site'
    message = '''
                Hello I am Tahir.
                Please help me out.
                I like it.
    '''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = []
    recipient_list.append(email)
    send_mail( subject, message, email_from, recipient_list )
    return JsonResponse({"status":"True", "message":"Email has been sent."})

    
    
