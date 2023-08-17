from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from users.models import User
from users.admin import NormUserCreationForm
from departments.models import Department
from centres.models import Centre
from vehicles.models import Vehicle
from vehicles.admin import VehicleCreationForm

from movement.models import Movement

@login_required
def home(request):
    users = []
    vehicles = []
    mov_in = []
    mov_all = []
    results = ""

    all_centres = [ x[0] for x in Centre.objects.all().values_list("code") ]
    all_departments = [ x[0] for x in Department.objects.all().values_list("name")]
    datetime = timezone.now()

    if request.method == "GET":
        if "query" in request.GET:
            query = request.GET.get("query")

            vehicles = Vehicle.objects.filter(vehicle_no=query)
            if len(vehicles) > 0:
                for vehicle in vehicles:
                    users.append(vehicle.user)
            else:
                users = User.objects.filter(badge=query)
                for user in users:
                    vehicles = Vehicle.objects.filter(user=user)
            if len(users) == 0:
                results = "-- User not found! --"

            if request.GET.get("clock") is not None:
                clock = int(request.GET.get("clock"))
                if len(users) > 0:
                    mov = Movement.objects.filter(user=users[0], out_time=None)
                    
                    if len(mov) == 1 and clock == 0:
                        Movement.objects.filter(user=users[0], out_time=None).update(out_time=timezone.now())
                    elif len(mov) == 0 and clock == 1:
                        if len(users) > 0 and len(vehicles) > 0:
                            mov = Movement(user=users[0], vehicle=vehicles[0])
                            mov.save()
                        elif len(users) > 0:
                            mov = Movement(user=users[0])
                            mov.save()
                        elif len(vehicles) > 0:
                            mov = Movement(vehicle=vehicles[0])
                            mov.save()

    mov_in = Movement.objects.filter(out_time=None)
    mov_all = Movement.objects.filter(date=timezone.now())
        
    if request.method == "POST":
        user_create_form = NormUserCreationForm(request.POST)
        vh_create_form = VehicleCreationForm(request.POST)
        
        if user_create_form.is_valid():
            user_create_form.save()
            results = " -- User successfully created! --"
        else:
            results = " -- User creation Failed! -- "
        
        if vh_create_form.is_valid():
            vh_create_form.save()
            results = " -- Vehcile successfully created! --"
        else:
            results = " -- Vehcile creation Failed! -- "

    context = {"users": users,
                "vehicles": vehicles,
                "departments": all_departments,
                "centres": all_centres,
                "movement_in": mov_in,
                "movement_all": mov_all,
                "date": datetime,
                "results": results,
                "user_form": NormUserCreationForm,
                "vh_form": VehicleCreationForm}

    return render(request, "home.html", context=context)

def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        badge = request.POST.get("badge")
        password = request.POST.get("password")
        user = authenticate(request, badge=badge, password=password)
        if user is None:
            context = {"error": "Invalid badge or password"}
            return render(request, "login.html", context=context)
        login(request, user)
        return redirect('/')
    return render(request, "login.html")

def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect('/login/')
    return render(request, "login.html")
